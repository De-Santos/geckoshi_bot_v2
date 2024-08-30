from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import cache
import settings
from chat_processor.member import check_membership
from database import get_session, User, save_user, is_user_exists_by_tg, update_user_language, update_user_is_bot_start_completed_by_tg_id, is_good_user_by_tg, Setting, SettingsKey, is_admin
from filters.base_filters import UserExistsFilter, IsGoodUserFilter
from handlers.referral import process_paying_for_referral
from keyboard_markup.custom_user_kb import get_reply_keyboard_kbm
from keyboard_markup.inline_user_kb import get_lang_kbm, get_require_subscription_kbm, get_user_menu_kbm
from lang.lang_based_provider import MessageKey as msgK, MessageKey, Lang, get_keyboard, format_string
from lang.lang_based_provider import get_message
from lang.lang_provider import cache_lang, get_cached_lang
from lang_based_variable import LangSetCallback, CheckStartMembershipCallback, KeyboardKey, BackToMenu
from providers.tg_arg_provider import TgArg, ArgType
from states.states import StartStates

router = Router(name="start_router")


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    session = get_session()
    if not await is_user_exists_by_tg(session, message.from_user.id, cache_id=message.from_user.id):
        ref_arg = TgArg.get_arg(ArgType.REFERRAL, message.text)
        if ref_arg is not None and await is_good_user_by_tg(session, ref_arg.get(), cache_id=ref_arg.get()):
            user = User(telegram_id=message.from_user.id, referred_by_id=ref_arg.get())
            await bot.send_message(chat_id=ref_arg.get(), text=format_string(get_message(MessageKey.REF_INVITED_STEP_ONE, await get_cached_lang(ref_arg.get())),
                                                                             user_link=message.from_user.id,
                                                                             amount=await settings.get_setting(SettingsKey.PAY_FOR_REFERRAL)))
        else:
            user = User(telegram_id=message.from_user.id)
        save_user(session, user)
        await state.set_state(StartStates.language)
        await message.answer(get_message(msgK.START), reply_markup=get_lang_kbm())
        await cache.drop_cache(is_user_exists_by_tg, cache_id=message.from_user.id)
    else:
        await message.answer(text=get_message(msgK.START),
                             reply_markup=get_reply_keyboard_kbm(Lang.EN, await is_admin(session, message.from_user.id)))
        await message.delete()


@router.callback_query(LangSetCallback.filter(), StartStates.language, UserExistsFilter())
async def change_lang_handler(query: CallbackQuery, callback_data: LangSetCallback,
                              state: FSMContext) -> None:
    session = get_session()
    update_user_language(session, query.from_user.id, callback_data.lang)
    await query.answer(text=get_message(MessageKey.LANG_CHANGE, callback_data.lang))
    await cache_lang(query.from_user.id, callback_data.lang)
    await state.set_state(StartStates.subscription)
    await query.message.delete()
    await require_subscription(query.message, callback_data.lang)


@router.message(StartStates.subscription, UserExistsFilter())
async def require_subscription(message: types.Message, lang: Lang) -> None:
    await message.answer(text=get_message(MessageKey.START_REQUIRE_SUBSCRIPTION, lang),
                         reply_markup=get_require_subscription_kbm(lang))


def get_ids(kbk: KeyboardKey, lang: Lang) -> list[str]:
    markup = get_keyboard(kbk, lang)
    ids = []
    for row in markup:
        for kb in row:
            if kb.id_ is not None:
                ids.append(kb.id_)
    return ids


@router.callback_query(CheckStartMembershipCallback.filter(), StartStates.subscription, UserExistsFilter())
async def check_subscription(query: CallbackQuery, callback_data: CheckStartMembershipCallback, state: FSMContext,
                             lang: Lang, is_admin: bool, bot: Bot) -> None:
    r = [await check_membership(query.from_user.id, link) for link in get_ids(callback_data.kbk, callback_data.lang)]
    if False in r:
        await query.message.answer(text=get_message(MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED, lang))
        await require_subscription(query.message, callback_data.lang)
    else:
        await state.clear()
        update_user_is_bot_start_completed_by_tg_id(get_session(), query.from_user.id, True)
        await query.message.delete()
        await query.message.answer(text=get_message(MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL, lang),
                                   reply_markup=get_reply_keyboard_kbm(lang, is_admin))
        await process_paying_for_referral(query.from_user.id, bot)


@router.callback_query(BackToMenu.filter(), IsGoodUserFilter())
async def back_to_menu(query: CallbackQuery, callback_data: BackToMenu, state: FSMContext, lang: Lang):
    await state.clear()
    if callback_data.remove_source:
        await query.message.delete()
    await query.message.answer(text=get_message(MessageKey.MENU_MESSAGE, lang),
                               reply_markup=get_user_menu_kbm(lang))


@router.message(F.text == "/menu", IsGoodUserFilter())
async def menu(message: types.Message, lang: Lang, state: FSMContext) -> None:
    await message.delete()
    await state.clear()
    await message.answer(text=get_message(MessageKey.MENU_MESSAGE, lang),
                         reply_markup=get_user_menu_kbm(lang))


@router.message(F.text == "/aaa", IsGoodUserFilter())
async def test(message) -> None:
    session = get_session()
    # TEMP TODO: DELETE ME
    session.add(Setting(id=SettingsKey.PAY_FOR_REFERRAL, int_val=1500))
    session.add(Setting(id=SettingsKey.MIN_WITHDRAW_IN_AIRDROP, int_val=0))
    session.add(Setting(id=SettingsKey.PREMIUM_GMEME_PRICE, int_val=30000))
    session.commit()
