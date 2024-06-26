from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import cache
from callbacks.start import LangSetCallback, CheckStartMembershipCallback
from chat_processor.member import check_membership
from database import get_session, User, save_user, is_good_user, is_user_exists_by_tg, update_user_language, \
    update_user_is_bot_start_completed_by_tg_id
from filters.base_filters import UserExistsFilter, IsGoodUserFilter, ChatTypeFilter
from keyboard_markup.custom_user_kb import get_reply_keyboard_kbm
from keyboard_markup.inline_user_kb import get_start_user_kbm, get_require_subscription_kbm, get_user_menu_kbm
from lang.lang_based_text_provider import MessageKey as msgK, MessageKey, Lang, get_keyboard
from lang.lang_based_text_provider import get_message
from lang.lang_provider import cache_lang
from middleware.metadata_providers import LangProviderMiddleware, IsAdminProviderMiddleware
from providers.tg_arg_provider import TgArg, ArgType
from states.start import StartStates

router = Router(name="start_router")

router.message.middleware(LangProviderMiddleware())
router.callback_query.middleware(LangProviderMiddleware())

router.message.middleware(IsAdminProviderMiddleware())
router.callback_query.middleware(IsAdminProviderMiddleware())

router.message.filter(ChatTypeFilter())
router.callback_query.filter(ChatTypeFilter())


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    session = get_session()
    if not await is_user_exists_by_tg(session, message.from_user.id, cache_id=message.from_user.id):
        ref_arg = TgArg.get_arg(ArgType.REFERRAL, message.text)
        if ref_arg is not None and is_good_user(session, ref_arg.get()):
            user = User(telegram_id=message.from_user.id, referred_by_id=ref_arg.get())
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
    await query.answer(text=get_message(MessageKey.lANG_CHANGE, callback_data.lang))
    await cache_lang(query.from_user.id, callback_data.lang)
    await state.set_state(StartStates.subscription)
    await query.message.delete()
    await require_subscription(query.message, callback_data.lang)


@router.message(StartStates.subscription, UserExistsFilter())
async def require_subscription(message: types.Message, lang: Lang) -> None:
    await message.answer(text=get_message(MessageKey.START_REQUIRE_SUBSCRIPTION, lang),
                         reply_markup=get_require_subscription_kbm(lang))


@router.callback_query(CheckStartMembershipCallback.filter(), UserExistsFilter(), StartStates.subscription)
async def check_subscription(query: CallbackQuery, callback_data: CheckStartMembershipCallback, state: FSMContext,
                             lang: Lang, is_admin: bool) -> None:
    kbs = get_keyboard(callback_data.kbk, callback_data.lang)
    chat_ids = [kbs.get(i).get('id') for i in range(1, 4)]
    r = [await check_membership(query.from_user.id, link) for link in chat_ids]
    if False in r:
        await query.message.answer(text=get_message(MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED, lang))
        await require_subscription(query.message, callback_data.lang)
    else:
        await state.clear()
        session = get_session()
        update_user_is_bot_start_completed_by_tg_id(session, query.from_user.id, True)
        await query.message.delete()
        await query.message.answer(text=get_message(MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL, lang),
                                   reply_markup=get_reply_keyboard_kbm(lang, is_admin))
        # TODO: add paying if it's a referral user


@router.message(IsGoodUserFilter(), F.text == "/menu")
async def menu(message: types.Message, lang: Lang) -> None:
    await message.delete()
    await message.answer(text=get_message(MessageKey.MENU_MESSAGE, lang),
                         reply_markup=get_user_menu_kbm(lang))
