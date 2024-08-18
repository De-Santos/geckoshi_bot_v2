from enum import Enum
from typing import Any

from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel


class Lang(Enum):
    RU = "russian"
    EN = "english"
    TR = "turkish"
    DE = "german"


class MessageKey(Enum):
    START = "start"
    LANG_CHANGE = "lang_change"
    START_REQUIRE_SUBSCRIPTION = "start_required_subscription"
    START_REQUIRE_SUBSCRIPTION_SUCCESSFUL = "start_required_subscription_successful"
    START_REQUIRE_SUBSCRIPTION_FAILED = "start_required_subscription_failed"
    MENU_MESSAGE = "menu_message"
    REF_INVITED_STEP_ONE = "ref_invited_1"
    REF_INVITED_STEP_TWO = "ref_invited_2"
    REF_INVITE = "ref_invite"
    USER_PROFILE = "user_profile"
    LANG_MENU = "lang_menu"
    FUNCTION_NOT_IMPLEMENTED = "function_not_implemented"
    PREMIUM_ALREADY_BOUGHT = "premium_already_bought"
    PREMIUM_BUY_MENU = "premium_buy_menu"
    NOT_ENOUGH_TO_BUY_PREMIUM = "not_enough_to_buy_premium"
    PREMIUM_HAS_BOUGHT = "premium_has_bought"
    SOON = "soon"
    ADMIN_PANEL = "admin_panel"
    ADMIN_NOW = "admin_now"
    ADMIN_CHANGE_REF_PAY = "admin_change_ref_pay"
    ADMIN_CHANGE_REF_PAY_SUCCESSFULLY = "admin_change_ref_pay_successfully"
    ADMIN_ENTER_MAILING_MESSAGE = "admin_enter_mailing_message"
    ADMIN_MAILING_HAS_INLINE_BUTTON = "admin_mailing_has_inline_button"
    ADMIN_ENTER_INLINE_BUTTON_TEXT = "admin_enter_inline_button_text"
    ADMIN_ENTER_INLINE_BUTTON_URL = "admin_enter_inline_button_url"
    ADMIN_ADD_INLINE_BUTTON = "admin_add_inline_button"
    ADMIN_INLINE_BUTTON_PREVIEW = "admin_inline_button_preview"
    ADMIN_MAILING_MESSAGE_LOOKS_LIKE = "admin_mailing_message_looks_like"
    ADMIN_MAILING_STATS = "admin_mailing_stats"
    REQUEST_PROCESSING = "request_processing"
    ADMIN_MAILING_CANCEL_FAILED = "admin_mailing_cancel_failed"
    ADMIN_MAILING_CANCEL_SUCCESSFUL = "admin_mailing_cancel_successful"
    ADMIN_MAILING_FAILED_TO_SEND_MESSAGES_IN_QUEUE = "admin_mailing_start_retry"
    SLOTS_GAME_MENU = "slots_game_menu"
    SLOTS_NOT_ENOUGH_TO_PLAY = "slots_not_enough_to_play"
    SLOTS_WIN = "slots_win"
    SLOTS_LOSS = "slots_loss"
    ADMIN_TASK_MENU = "admin_task_menu"
    ADMIN_TASK_TYPE_SELECT = "admin_task_type_select"
    ADMIN_TASK_TITLE_REQUEST = "admin_task_title_request"
    ADMIN_TASK_TEXT_REQUEST = "admin_task_text_request"
    ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST = "admin_task_chat_subscription_require_request"
    ADMIN_TASK_EXPIRE_TIME_REQUEST = "admin_task_expire_time_request"
    ADMIN_TASK_GMEME_DONE_REWARD_REQUEST = "admin_task_gmeme_done_reward_request"
    ADMIN_TASK_BMEME_DONE_REWARD_REQUEST = "admin_task_bmeme_done_reward_request"
    TIME_BASED_TASK = "time_based_task"
    ADMIN_TASK_SAVED_SUCCESSFULLY = "admin_task_saved_successfully"
    ADMIN_TASK_ID_REQUEST = "admin_task_id_request"
    ADMIN_CONFIRM_TASK_DELETE = "admin_confirm_task_delete"
    ADMIN_TASK_DELETED_SUCCESSFULLY = "admin_task_deleted_successfully"
    CHOOSE_TASK_TYPE = "choose_task_type"
    TASK_ENDED = "task_ended"
    TASK_DONE_SUCCESSFULLY = "task_done_successfully"
    TASK_DONE_UNSUCCESSFULLY = "task_done_unsuccessfully"
    TASK_ALREADY_HAS_DONE = "task_already_has_done"


class KeyboardKey(Enum):
    START_REQUIRE_SUBSCRIPTION_KB = "start_required_subscription"
    MENU = "menu"
    ADMIN_MENU = "admin_menu"
    INLINE_MENU = "inline_menu"
    REF_LINK_SHARE = "ref_link_share"
    PROFILE = "profile"
    EXIT = "exit"
    STEP_BACK = "step_back"
    BUY_PREMIUM_MENU = "buy_premium_menu"
    ADMIN_PANEL = "admin_panel"
    YES_NO = "yes_no"
    ADMIN_ADD_BUTTON_OR_PREVIEW = "admin_mailing_add_button_or_preview"
    ADMIN_ADD_MORE_BUTTONS_OR_CONTINUE = "admin_add_more_buttons"
    ADMIN_INLINE_BUTTON_PREVIEW = "admin_inline_button_preview"
    ADMIN_MAILING_START = "admin_mailing_start"
    ADMIN_MAILING_MENU = "admin_mailing_menu"
    ADMIN_MAILING_QUEUE_FILL_RETRY = "admin_mailing_queue_fill_retry"
    SLOTS_MENU = "slots_menu"
    SLOTS_CONTINUE_PLAY = "slots_continue_play"
    BACK_TO_MENU = "back_to_menu"
    TASK_MENU = "task_menu"
    ADMIN_TASK_TYPE_MENU = "admin_task_type_menu"
    TASK_TYPE_MENU = "task_type_menu"
    RETRY = "retry"
    CONTINUE_OR_RETRY = "continue_or_retry"
    SAVE = "save"
    DELETE_TASK_MENU = "delete_task_menu"
    SELECT_TASK_NAV_MENU = "select_task_nav_menu"


class M(BaseModel):
    id_: str = None
    text: str
    url: str = None
    with_url_placeholder: bool = False
    callback_class: Any = None
    with_callback_param_required: bool = False
    with_text_param_required: bool = False

    def text(self, text: str) -> "M":
        self.text = text
        return self

    def get_callback_instance(self, **kwargs) -> Any:
        return self.callback_class(**kwargs)


class MenuToRefCallback(CallbackData, prefix="menu-to-ref"):
    pass


class MenuToBonusCallback(CallbackData, prefix="menu-to-bonus"):
    pass


class MenuToTasksCallback(CallbackData, prefix="menu-to-tasks"):
    pass


class MenuToChequeCallback(CallbackData, prefix="menu-to-cheque"):
    pass


class MenuToP2PCallback(CallbackData, prefix="menu-to-bonus"):
    pass


class MenuToSlotsCallback(CallbackData, prefix="menu-to-slots"):
    pass


class MenuToNFTCallback(CallbackData, prefix="menu-to-nft"):
    pass


class MenuToProfileCallback(CallbackData, prefix="menu-to-profile"):
    pass


class MenuToStatistic(CallbackData, prefix="menu-to-statistic"):
    pass


class LangSetCallback(CallbackData, prefix="set-lang"):
    lang: Lang


class CheckStartMembershipCallback(CallbackData, prefix="check-start-membership"):
    kbk: KeyboardKey
    lang: Lang


class ProfileWithdraw(CallbackData, prefix="profile-withdraw"):
    pass


class BuyPremiumMenu(CallbackData, prefix="buy-premium-menu"):
    pass


class BuyPremium(CallbackData, prefix="buy-premium"):
    pass


class ActivateVoucher(CallbackData, prefix="activate-voucher"):
    pass


class SetLangMenu(CallbackData, prefix="set-lang-menu"):
    pass


class Exit(CallbackData, prefix="exit"):
    pass


class StepBack(CallbackData, prefix="step-back"):
    pass


class MailingCallback(CallbackData, prefix="mailing"):
    pass


class UserManagement(CallbackData, prefix="user-management"):
    pass


class CreateVoucher(CallbackData, prefix="create-voucher"):
    pass


class TaskMenu(CallbackData, prefix="task-menu"):
    pass


class ChangeRefPay(CallbackData, prefix="change-ref-pay"):
    pass


class RefTop(CallbackData, prefix="ref-top"):
    duration: int | None


class Yes(CallbackData, prefix="yes"):
    pass


class No(CallbackData, prefix="no"):
    pass


class AddMoreInlineButton(CallbackData, prefix="add-more-inline-button"):
    pass


class MailingMessagePreview(CallbackData, prefix="mailing-message-preview"):
    pass


class ApproveInlineButton(CallbackData, prefix="approve-inline-button"):
    pass


class StartMailing(CallbackData, prefix="start-mailing"):
    pass


class StopMailing(CallbackData, prefix="stop-mailing"):
    mailing_id: int


class QueueFillMailingRetry(CallbackData, prefix="queue-fill-retry"):
    mailing_id: int


class UpdateMailingStatistic(CallbackData, prefix="update-mailing-stat"):
    mailing_id: int


class SlotsPlay(CallbackData, prefix="slots-play"):
    amount: int


class InlineKeyboardChange(CallbackData, prefix="inline-keyboard-change"):
    pass


class BackToMenu(CallbackData, prefix="back-to-menu"):
    remove_source: bool


class CreateTask(CallbackData, prefix="create-task"):
    pass


class DeleteTaskMenu(CallbackData, prefix="delete-task-menu"):
    pass


class StartCreatingTask(CallbackData, prefix="start-creating-task"):
    task_type: int


class Continue(CallbackData, prefix="continue"):
    pass


class Retry(CallbackData, prefix="retry"):
    pass


class Save(CallbackData, prefix="save"):
    pass


class DeleteTask(CallbackData, prefix="delete-task"):
    task_id: int


class TaskSelect(CallbackData, prefix="task-select"):
    task_type: int
    offset: int
    disabled: bool = False


class TaskDone(CallbackData, prefix="task-done"):
    task_id: int


message_data = {
    MessageKey.START: """<b>Geckoshi Аирдроп первый в мире инвестиционной мем монеты 🦎 Ниже выберите подходящий вам язык 🌐 и начните зарабатывать $GMEME прямо сейчас!\n\n____\n\n\nGeckoshi Airdrop the world's first investment meme coin 🦎 Below, select the lang that suits you 🌐 and start earning $GMEME right now!</b>""",

    Lang.RU: {
        MessageKey.LANG_CHANGE: "Язык успешно изменён на русский !",
        MessageKey.START_REQUIRE_SUBSCRIPTION: "<b>🦎 Для продолжения вы должны быть подписаны на наши каналы:</b>",
        MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL: "✅ Вы успешно подписались!",
        MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED: "⛔️ Подпишитесь на наши каналы и попробуйте ещё раз!",
        MessageKey.MENU_MESSAGE: "<b>🦎 В этом боте ты можешь:</b>",
        MessageKey.REF_INVITED_STEP_ONE: "👥 Вы пригласили <a href=\"tg://user?id={user_link}\">друга!</a> Вы получите 1500 $GMEME, как только ваш друг подпишется на каналы!",
        MessageKey.REF_INVITED_STEP_TWO: "👥 Вы получили {amount} $GMEME за регистрацию вашего <a href=\"tg://user?id={user_link}\">друга</a> в боте",
        MessageKey.REF_INVITE: """👥 Приглашай друзей и получай по {ref_invite_pay} $GMEME\n\n🔗 Твоя ссылка: <code>https://t.me/gcococococotest_bot?start={link}</code>\n\n🗣 Ты всего пригласил: {ref_invite_count} чел""",
        MessageKey.USER_PROFILE: """📝 Имя: <a href=\"tg://user?id={user_link}\">{user_name}</a>\n🆔 Ваш ID: <code>{user_tg_id}</code>\n🔥 Премиум аккаунт: {is_premium_account}\n💎 Баланс: {balance} $GMEME\n👥 Всего рефералов: {ref_count}\n🦎 ВЫВЕДЕНО: {withdrew} $GMEME\n<b>📣 Мы сообщим заранее о выплатах!\n🔥 Следите за новостями!\n⛔️ МИНИМАЛЬНЫЙ ВЫВОД БУДЕТ {min_withdraw_in_airdrop} В ДЕНЬ АИРДРОПА!</b>""",
        MessageKey.LANG_MENU: "Выберите желаемый язык:",
        MessageKey.FUNCTION_NOT_IMPLEMENTED: "К сожалению данная функция сейчас недоступна",
        MessageKey.PREMIUM_ALREADY_BOUGHT: "❗ У вас уже имеется Премиум!",
        MessageKey.PREMIUM_BUY_MENU: "🦎 Цена премиума: {premium_gmeme_price} $GMEME",
        MessageKey.NOT_ENOUGH_TO_BUY_PREMIUM: "❗ Для покупки не хватает {not_enough} $GMEME",
        MessageKey.PREMIUM_HAS_BOUGHT: "🥳 Вы приобрели \"Премиум\"",
        MessageKey.SOON: "Скоро 🔜",
        MessageKey.ADMIN_PANEL: "Админ-панель:\n\n🕰Аптайм бота: {uptime}\n👥Пользователей в боте: {user_count}",
        MessageKey.ADMIN_NOW: "Вам наданы права админестратора",
        MessageKey.ADMIN_CHANGE_REF_PAY: "Введите новвую сумму для вознограждения за реферала.\nТекущее значение: {pay_for_ref}",
        MessageKey.ADMIN_CHANGE_REF_PAY_SUCCESSFULLY: "Вознаграждение за реферала измененно на: {pay_for_ref}",
        MessageKey.ADMIN_ENTER_MAILING_MESSAGE: "Введите текст рассылки или отправьте изображение:",
        MessageKey.ADMIN_MAILING_HAS_INLINE_BUTTON: "Добавить плавающую кнопку-ссылку ?",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_TEXT: "Введите текст для плавающей кнопки-ссылки:",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_URL: "Введите url для плавающей кнопки-ссылки:",
        MessageKey.ADMIN_ADD_INLINE_BUTTON: "Плавающая кнопка-ссылка успешно добавлена!",
        MessageKey.ADMIN_INLINE_BUTTON_PREVIEW: "Кнопка будет выглядеть так:",
        MessageKey.ADMIN_MAILING_MESSAGE_LOOKS_LIKE: "^^^ - так будет выглядеть сообщение для рассылки.",
        MessageKey.ADMIN_MAILING_STATS: "Статистика рассылки №{mailing_id}:\n Юзеров захвачено: {user_captured}\n Статус: {status}\n Успешно: {successfully}\n В очереди: {in_queue}\n Неуспешно: {failed}\n Отменено: {canceled}\n Всего обработано: {messages_processed} ({messages_processed_percents})\n Время обработки: {processing_time}",
        MessageKey.REQUEST_PROCESSING: "Запрос обрабатываеться...",
        MessageKey.ADMIN_MAILING_CANCEL_FAILED: "Не возможно отменить рассылку.",
        MessageKey.ADMIN_MAILING_CANCEL_SUCCESSFUL: "Рассылка №{mailing_id} отменена успешно!",
        MessageKey.ADMIN_MAILING_FAILED_TO_SEND_MESSAGES_IN_QUEUE: "Произошла ошибка при добалвении сообщений в queue.",
        MessageKey.SLOTS_GAME_MENU: """Добро пожаловать в раздел слотов.\nЗдесь ты можешь выграть много денег, вот выйгрышные комбинации:\n1. 🦎🦎🦎 - x10\n2.  🏜️🏜️🏜️ - x5\n3. 🏖️🏖️🏖️ - x3\n4. 🏕️🏕️🏕️ - x2\n5. ✈️✈️✈️ - x1.8\n6. 🚀🚀🚀 - x1.7\n7. 🪲🪲🪲 - x1.5\n8. 🐞🐞🐞 - x1.2\n9. 🐝🐝🐝 - x1.05\nУдачи! - она тебе пригодиться.\nНа сколько $GMEME играем ?""",
        MessageKey.SLOTS_NOT_ENOUGH_TO_PLAY: "💲У тебя недостаточно баланса чтобы играть. Попробуй изменить сумму.",
        MessageKey.SLOTS_WIN: "🎉Поздравляем ты выиграл: {amount} $GMEME\n🎰Твоя выигрышная комбинация: {combination}",
        MessageKey.SLOTS_LOSS: "🃏К сожелению в этот раз тебе не повезло - ты проиграл ставку ({amount} $GMEME).\n🎰Твоя комбинация: {combination}\nПопробуй ещё раз, тебе обязательно повезёт!",
        MessageKey.ADMIN_TASK_MENU: "📋Выберите ваше дейвствие",
        MessageKey.ADMIN_TASK_TYPE_SELECT: "Выберете тип задания",
        MessageKey.ADMIN_TASK_TITLE_REQUEST: "Введите название задания:",
        MessageKey.ADMIN_TASK_TEXT_REQUEST: "Введите тект задания:",
        MessageKey.ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST: "Введите chat_id - каналов, груп, через запятую.",
        MessageKey.ADMIN_TASK_EXPIRE_TIME_REQUEST: "Введите время жизни задачи.\nexample: 10h",
        MessageKey.ADMIN_TASK_GMEME_DONE_REWARD_REQUEST: "Введите сумму вознаграждения в $GMEME.",
        MessageKey.ADMIN_TASK_BMEME_DONE_REWARD_REQUEST: "Введите сумму вознаграждения в $BMEME.",
        MessageKey.TIME_BASED_TASK: "<b>{title}</b>\n\nid: {task_id}\nОписание: {text}\nОплата: {done_reward} $GMEME\nОсталось времени: {expires_in}",
        MessageKey.ADMIN_TASK_SAVED_SUCCESSFULLY: "Задача с id: {task_id} была сохранена успешно",
        MessageKey.ADMIN_TASK_ID_REQUEST: "Введите айди задачи:",
        MessageKey.ADMIN_CONFIRM_TASK_DELETE: "^^^- удалть эту задачу ?",
        MessageKey.ADMIN_TASK_DELETED_SUCCESSFULLY: "Задача удалена успешно!",
        MessageKey.CHOOSE_TASK_TYPE: "🔥 В нашем боте вы можете заработать на наших заданиях!",
        MessageKey.TASK_ENDED: "😞 Задания кончились! Попробуйте позднее.",
        MessageKey.TASK_DONE_SUCCESSFULLY: "✅ Вы успешно выполнили задание {task_id}",
        MessageKey.TASK_DONE_UNSUCCESSFULLY: "❌ Вы не выполнили условия задания!",
        MessageKey.TASK_ALREADY_HAS_DONE: "❌ Вы уже выполнили это задание!",
    },
}
keyboard_data = {
    KeyboardKey.SLOTS_MENU: [
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
        [
            M(text="{amount} $GMEME", callback_class=SlotsPlay, with_callback_param_required=True, with_text_param_required=True),
        ],
    ],
    KeyboardKey.ADMIN_TASK_TYPE_MENU: [
        [
            M(text="🕑 time based", callback_class=StartCreatingTask, with_callback_param_required=True),
        ],
        [
            M(text="☑️ done based", callback_class=StartCreatingTask, with_callback_param_required=True),
        ],
        [
            M(text="💰 pool based", callback_class=StartCreatingTask, with_callback_param_required=True),
        ],
    ],
    KeyboardKey.TASK_TYPE_MENU: [
        [
            M(text="🕑 time based", callback_class=TaskSelect, with_callback_param_required=True),
        ],
        # [
        #     M(text="☑️ done based", callback_class=TaskSelect, with_callback_param_required=True),
        # ],
        # [
        #     M(text="💰 pool based", callback_class=TaskSelect, with_callback_param_required=True),
        # ],
    ],
    Lang.RU: {
        KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB: [
            [
                M(id_="@dropto_data", text="text 1", url="https://t.me/dropto_data"),
                M(id_="@dropto_data", text="text 1", url="https://t.me/dropto_data"),
            ],
            [
                M(id_="@dropto_data", text="text 1", url="https://t.me/dropto_data"),
            ],
            [
                M(text="✅ Подписался", callback_class=CheckStartMembershipCallback)
            ]
        ],
        KeyboardKey.MENU: [
            [
                M(text="/menu"),
            ]
        ],
        KeyboardKey.ADMIN_MENU: [
            [
                M(text="/admin_panel"),
            ]
        ],
        KeyboardKey.INLINE_MENU: [
            [
                M(text="💸 Заработать", callback_class=MenuToRefCallback),
                M(text="🎁 Бонус", callback_class=MenuToBonusCallback),
            ],
            [
                M(text="📣 Задания", callback_class=MenuToTasksCallback),
                M(text="🏷 Чеки", callback_class=MenuToChequeCallback),
            ],
            [
                M(text="🗳 P2P", callback_class=MenuToP2PCallback),
                M(text="🎰 Слоты", callback_class=MenuToSlotsCallback),
            ],
            [
                M(text="🧩 NFT", callback_class=MenuToNFTCallback),
                M(text="💼 Профиль", callback_class=MenuToProfileCallback),
            ],
            [
                M(text="📊 Статистика", callback_class=MenuToStatistic),
            ],
        ],
        KeyboardKey.REF_LINK_SHARE: [
            [
                M(text="🔗 Выслать приглашение", url="https://t.me/share/url?url=https://t.me/TeestttgeckoshiBot?start={ref_link}", with_url_placeholder=True)
            ]
        ],
        KeyboardKey.PROFILE: [
            [
                M(text="📤 Вывести", callback_class=ProfileWithdraw),
                M(text="🔥 Премиум", callback_class=BuyPremiumMenu)
            ],
            [
                M(text="🎟 Активировать промокод", callback_class=ActivateVoucher)
            ],
            [
                M(text="🔄 Изменить язык", callback_class=SetLangMenu)
            ],
        ],
        KeyboardKey.EXIT: [
            [
                M(text="❌ Выйти", callback_class=Exit)
            ]
        ],
        KeyboardKey.STEP_BACK: [
            [
                M(text="⬅️ Назад", callback_class=StepBack)
            ]
        ],
        KeyboardKey.BUY_PREMIUM_MENU: [
            [
                M(text="🔥 Купить премиум", callback_class=BuyPremium)
            ]
        ],
        KeyboardKey.ADMIN_PANEL: [
            [
                M(text="✉️ Рассылка", callback_class=MailingCallback),
                M(text="🔎 Управление", callback_class=UserManagement),
            ],
            [
                M(text="👥 Топ рефоводов", callback_class=RefTop, with_callback_param_required=True),
                M(text="за неделю", callback_class=RefTop, with_callback_param_required=True),
                M(text="👥 Плата за реф", callback_class=ChangeRefPay),
            ],
            [
                M(text="🦎 Создать промокод", callback_class=CreateVoucher),
                M(text="📝 Задание", callback_class=TaskMenu),
            ],
        ],
        KeyboardKey.YES_NO: [
            [
                M(text="Да", callback_class=Yes),
                M(text="Нет", callback_class=No)
            ]
        ],
        KeyboardKey.ADMIN_ADD_BUTTON_OR_PREVIEW: [
            [
                M(text="Добавить ещё кнопку", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Просмотреть сообщение", callback_class=MailingMessagePreview),
            ],
        ],
        KeyboardKey.ADMIN_ADD_MORE_BUTTONS_OR_CONTINUE: [
            [
                M(text="Добавить ещё кнопку", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Продолжить", callback_class=Continue),
            ],
        ],
        KeyboardKey.ADMIN_INLINE_BUTTON_PREVIEW: [
            [
                M(text="Добавить", callback_class=ApproveInlineButton),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_START: [
            [
                M(text="Начать рассылку", callback_class=StartMailing),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_MENU: [
            [
                M(text="Отменить рассылку", callback_class=StopMailing, with_callback_param_required=True),
                M(text="Обновить", callback_class=UpdateMailingStatistic, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_QUEUE_FILL_RETRY: [
            [
                M(text="Повторить поптыку", callback_class=QueueFillMailingRetry, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SLOTS_CONTINUE_PLAY: [
            [
                M(text="Повторить ставку", callback_class=SlotsPlay, with_callback_param_required=True),
            ],
            [
                M(text="Изменить ставку", callback_class=InlineKeyboardChange),
            ],
        ],
        KeyboardKey.BACK_TO_MENU: [
            [
                M(text="❌ Вернуться в меню", callback_class=BackToMenu, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.TASK_MENU: [
            [
                M(text="Создание", callback_class=CreateTask),
                M(text="Удаление", callback_class=DeleteTaskMenu),
            ],
        ],
        KeyboardKey.CONTINUE_OR_RETRY: [
            [
                M(text="Продолжить", callback_class=Continue),
                M(text="Повторить", callback_class=Retry),
            ],
        ],
        KeyboardKey.SAVE: [
            [
                M(text="Сохранить", callback_class=Save),
            ],
        ],
        KeyboardKey.DELETE_TASK_MENU: [
            [
                M(text="Удалить", callback_class=DeleteTask, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SELECT_TASK_NAV_MENU: [
            [
                M(text="✅ Проверить", callback_class=TaskDone, with_callback_param_required=True),
            ],
            [
                M(text="⬅️ Предыдущее", callback_class=TaskSelect, with_callback_param_required=True),
                M(text="Следующее ➡️", callback_class=TaskSelect, with_callback_param_required=True),
            ],
        ],
    },
}
