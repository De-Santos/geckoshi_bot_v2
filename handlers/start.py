from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import cache
from chat_processor.member import check_membership
from database import get_session, User, save_user, is_user_exists_by_tg, update_user_language, \
    update_user_is_bot_start_completed_by_tg_id, is_good_user_by_tg, get_user_by_tg, Settings, SettingsKey
from filters.base_filters import UserExistsFilter, IsGoodUserFilter
from keyboard_markup.custom_user_kb import get_reply_keyboard_kbm
from keyboard_markup.inline_user_kb import get_start_user_kbm, get_require_subscription_kbm, get_user_menu_kbm
from lang.lang_based_provider import MessageKey as msgK, MessageKey, Lang, get_keyboard
from lang.lang_based_provider import get_message
from lang.lang_provider import cache_lang, get_cached_lang
from lang_based_variable import LangSetCallback, CheckStartMembershipCallback, KeyboardKey
from providers.tg_arg_provider import TgArg, ArgType
from states.start import StartStates

router = Router(name="start_router")


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    session = get_session()
    if not await is_user_exists_by_tg(session, message.from_user.id, cache_id=message.from_user.id):
        ref_arg = TgArg.get_arg(ArgType.REFERRAL, message.text)
        if ref_arg is not None and await is_good_user_by_tg(session, ref_arg.get(), cache_id=ref_arg.get()):
            user = User(telegram_id=message.from_user.id, referred_by_id=ref_arg.get())
            await bot.send_message(chat_id=ref_arg.get(),
                                   text=get_message(MessageKey.REF_INVITED_STEP_ONE,
                                                    await get_cached_lang(ref_arg.get())).format(
                                       user_link=message.from_user.id))
        else:
            user = User(telegram_id=message.from_user.id)
        save_user(session, user)
        await state.set_state(StartStates.language)
        await message.answer(get_message(msgK.START), reply_markup=get_start_user_kbm())
        await cache.drop_cache(is_user_exists_by_tg, cache_id=message.from_user.id)
    else:
        await message.delete()


@router.callback_query(UserExistsFilter(), LangSetCallback.filter(), StartStates.language)
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


@router.callback_query(CheckStartMembershipCallback.filter(), UserExistsFilter(), StartStates.subscription)
async def check_subscription(query: CallbackQuery, callback_data: CheckStartMembershipCallback, state: FSMContext,
                             lang: Lang, is_admin: bool) -> None:
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
        user: User = get_user_by_tg(get_session(), query.from_user.id)


@router.message(IsGoodUserFilter(), F.text == "/menu")
async def menu(message: types.Message, lang: Lang) -> None:
    await message.delete()
    await message.answer(text=get_message(MessageKey.MENU_MESSAGE, lang),
                         reply_markup=get_user_menu_kbm(lang))


@router.message(IsGoodUserFilter(), F.text == "/aaa")
async def test() -> None:
    session = get_session()
    # TEMP TODO: DELETE ME
    session.add(Settings(id=SettingsKey.PAY_FOR_REFERRAL, int_val=1500))
    session.commit()
