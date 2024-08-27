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
    BONUS_TASK = "bonus_task"
    ADMIN_TASK_SAVED_SUCCESSFULLY = "admin_task_saved_successfully"
    ADMIN_TASK_ID_REQUEST = "admin_task_id_request"
    ADMIN_CONFIRM_TASK_DELETE = "admin_confirm_task_delete"
    ADMIN_TASK_DELETED_SUCCESSFULLY = "admin_task_deleted_successfully"
    CHOOSE_TASK_TYPE = "choose_task_type"
    CHOOSE_BONUS = "choose_bonus"
    TASK_ENDED = "task_ended"
    BONUS_TASK_ENDED = "bonus_task_ended"
    TASK_DONE_SUCCESSFULLY = "task_done_successfully"
    TASK_DONE_UNSUCCESSFULLY = "task_done_unsuccessfully"
    TASK_ALREADY_HAS_DONE = "task_already_has_done"
    PUBLIC_STATISTIC = "public_statistic"


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
    SELECT_TASK_SUBMIT_BUTTON = "select_task_submit_button"
    SELECT_TASK_NAV_MENU = "select_task_nav_menu"
    PAGINATION_MENU = "pagination_menu"
    BONUS_TASK_BUTTON = "bonus_task_button"
    SKIP = "skip"


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


class MenuToP2PCallback(CallbackData, prefix="menu-to-p2p"):
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
    page: int
    disabled: bool = False


class BonusTaskSelect(CallbackData, prefix="bonus-task-select"):
    task_id: int


class PaginationMove(CallbackData, prefix="pagination-move"):
    page: int
    disabled: bool = False


class TaskDone(CallbackData, prefix="task-done"):
    task_id: int


class Skip(CallbackData, prefix="skip"):
    pass


class Void(CallbackData, prefix="_"):
    pass


message_data = {
    MessageKey.START: """<b>Geckoshi Аирдроп первый в мире инвестиционной мем монеты 🦎 Ниже выберите подходящий вам язык 🌐 и начните зарабатывать $GMEME прямо сейчас!\n\n____\n\n\nGeckoshi Airdrop the world's first investment meme coin 🦎 Below, select the lang that suits you 🌐 and start earning $GMEME right now!</b>""",

    Lang.RU: {
        MessageKey.LANG_CHANGE: "Язык успешно изменён на русский !",
        MessageKey.START_REQUIRE_SUBSCRIPTION: "<b>🦎 Для продолжения вы должны быть подписаны на наши каналы:</b>",
        MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL: "✅ Вы успешно подписались!",
        MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED: "⛔️ Подпишитесь на наши каналы и попробуйте ещё раз!",
        MessageKey.MENU_MESSAGE: "<b>🦎 В этом боте ты можешь:</b>",
        MessageKey.REF_INVITED_STEP_ONE: "👥 Вы пригласили <a href=\"tg://user?id={user_link}\">друга!</a> Вы получите {amount} $GMEME, как только ваш друг подпишется на каналы!",
        MessageKey.REF_INVITED_STEP_TWO: "👥 Вы получили {amount} $GMEME за регистрацию вашего <a href=\"tg://user?id={user_link}\">друга</a> в боте",
        MessageKey.REF_INVITE: """👥 Приглашай друзей и получай по {ref_invite_pay} $GMEME\n\n🔗 Твоя ссылка: <code>https://t.me/Geckoshi_bot?start={link}</code>\n\n🗣 Ты всего пригласил: {ref_invite_count} чел""",
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
        MessageKey.SLOTS_LOSS: "🃏К сожалению в этот раз тебе не повезло - ты проиграл ставку ({amount} $GMEME).\n🎰Твоя комбинация: {combination}\nПопробуй ещё раз, тебе обязательно повезёт!",
        MessageKey.ADMIN_TASK_MENU: "📋Выберите ваше дейвствие",
        MessageKey.ADMIN_TASK_TYPE_SELECT: "Выберете тип задания",
        MessageKey.ADMIN_TASK_TITLE_REQUEST: "Введите название задания:",
        MessageKey.ADMIN_TASK_TEXT_REQUEST: "Введите тект задания:",
        MessageKey.ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST: "Введите chat_id - каналов, груп, через запятую.",
        MessageKey.ADMIN_TASK_EXPIRE_TIME_REQUEST: "Введите время жизни задачи.\nexample: 10h",
        MessageKey.ADMIN_TASK_GMEME_DONE_REWARD_REQUEST: "Введите сумму вознаграждения в $GMEME.",
        MessageKey.ADMIN_TASK_BMEME_DONE_REWARD_REQUEST: "Введите сумму вознаграждения в $BMEME.",
        MessageKey.TIME_BASED_TASK: "<b>{title}</b>\n\nid: {task_id}\nОписание: {text}\nОплата: {done_reward} $GMEME\nОсталось времени: {expires_in}",
        MessageKey.BONUS_TASK: "<b>{title}</b>\n\nОписание:\n{text}\nОплата: {done_reward} $GMEME",
        MessageKey.ADMIN_TASK_SAVED_SUCCESSFULLY: "Задача с id: {task_id} была сохранена успешно",
        MessageKey.ADMIN_TASK_ID_REQUEST: "Введите айди задачи:",
        MessageKey.ADMIN_CONFIRM_TASK_DELETE: "^^^- удалть эту задачу ?",
        MessageKey.ADMIN_TASK_DELETED_SUCCESSFULLY: "Задача удалена успешно!",
        MessageKey.CHOOSE_TASK_TYPE: "🔥 В нашем боте вы можете заработать на наших заданиях!",
        MessageKey.CHOOSE_BONUS: "🎁 Выберете бонусное задание которое хотите выполнить:",
        MessageKey.TASK_ENDED: "😞 Задания кончились! Попробуйте позднее.",
        MessageKey.BONUS_TASK_ENDED: "😞 К сожаленю, сейчас нет бонусных заданий для вас. Попробуйте позднее.",
        MessageKey.TASK_DONE_SUCCESSFULLY: "✅ Вы успешно выполнили задание №{task_id}",
        MessageKey.TASK_DONE_UNSUCCESSFULLY: "❌ Вы не выполнили условия задания!",
        MessageKey.TASK_ALREADY_HAS_DONE: "❌ Вы уже выполнили это задание!",
        MessageKey.PUBLIC_STATISTIC: "📊 <b>Статистика проекта:</b>\n\n👥 Всего пользователей: {total_users}\n👤 Новых за сегодня: {today_joined}",
    },
    Lang.EN: {
        MessageKey.LANG_CHANGE: "Language successfully changed to English!",
        MessageKey.START_REQUIRE_SUBSCRIPTION: "<b>🦎 To continue, you must be subscribed to our channels:</b>",
        MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL: "✅ You have successfully subscribed!",
        MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED: "⛔️ Please subscribe to our channels and try again!",
        MessageKey.MENU_MESSAGE: "<b>🦎 In this bot, you can:</b>",
        MessageKey.REF_INVITED_STEP_ONE: "👥 You have invited <a href=\"tg://user?id={user_link}\">a friend!</a> You will receive {amount} $GMEME once your friend subscribes to the channels!",
        MessageKey.REF_INVITED_STEP_TWO: "👥 You received {amount} $GMEME for registering your <a href=\"tg://user?id={user_link}\">friend</a> in the bot",
        MessageKey.REF_INVITE: """👥 Invite friends and earn {ref_invite_pay} $GMEME\n\n🔗 Your link: <code>https://t.me/Geckoshi_bot?start={link}</code>\n\n🗣 You have invited: {ref_invite_count} people in total""",
        MessageKey.USER_PROFILE: """📝 Name: <a href=\"tg://user?id={user_link}\">{user_name}</a>\n🆔 Your ID: <code>{user_tg_id}</code>\n🔥 Premium account: {is_premium_account}\n💎 Balance: {balance} $GMEME\n👥 Total referrals: {ref_count}\n🦎 WITHDRAWN: {withdrew} $GMEME\n<b>📣 We will notify you in advance about payouts!\n🔥 Stay tuned for updates!\n⛔️ MINIMUM WITHDRAWAL WILL BE {min_withdraw_in_airdrop} ON AIRDROP DAY!</b>""",
        MessageKey.LANG_MENU: "Choose your preferred language:",
        MessageKey.FUNCTION_NOT_IMPLEMENTED: "Unfortunately, this function is currently unavailable",
        MessageKey.PREMIUM_ALREADY_BOUGHT: "❗ You already have Premium!",
        MessageKey.PREMIUM_BUY_MENU: "🦎 Premium price: {premium_gmeme_price} $GMEME",
        MessageKey.NOT_ENOUGH_TO_BUY_PREMIUM: "❗ You don't have enough {not_enough} $GMEME to buy Premium",
        MessageKey.PREMIUM_HAS_BOUGHT: "🥳 You have purchased 'Premium'",
        MessageKey.SOON: "Coming soon 🔜",
        MessageKey.ADMIN_PANEL: "Admin panel:\n\n🕰Bot uptime: {uptime}\n👥Users in bot: {user_count}",
        MessageKey.ADMIN_NOW: "You have been granted administrator rights",
        MessageKey.ADMIN_CHANGE_REF_PAY: "Enter the new reward amount for referrals.\nCurrent value: {pay_for_ref}",
        MessageKey.ADMIN_CHANGE_REF_PAY_SUCCESSFULLY: "Referral reward has been changed to: {pay_for_ref}",
        MessageKey.ADMIN_ENTER_MAILING_MESSAGE: "Enter the mailing text or send an image:",
        MessageKey.ADMIN_MAILING_HAS_INLINE_BUTTON: "Add an inline button with a link?",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_TEXT: "Enter the text for the inline button:",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_URL: "Enter the URL for the inline button:",
        MessageKey.ADMIN_ADD_INLINE_BUTTON: "Inline button successfully added!",
        MessageKey.ADMIN_INLINE_BUTTON_PREVIEW: "The button will look like this:",
        MessageKey.ADMIN_MAILING_MESSAGE_LOOKS_LIKE: "^^^ - this is what the mailing message will look like.",
        MessageKey.ADMIN_MAILING_STATS: "Mailing statistics №{mailing_id}:\n Users reached: {user_captured}\n Status: {status}\n Successful: {successfully}\n In queue: {in_queue}\n Failed: {failed}\n Canceled: {canceled}\n Total processed: {messages_processed} ({messages_processed_percents})\n Processing time: {processing_time}",
        MessageKey.REQUEST_PROCESSING: "Request is being processed...",
        MessageKey.ADMIN_MAILING_CANCEL_FAILED: "Unable to cancel mailing.",
        MessageKey.ADMIN_MAILING_CANCEL_SUCCESSFUL: "Mailing №{mailing_id} successfully canceled!",
        MessageKey.ADMIN_MAILING_FAILED_TO_SEND_MESSAGES_IN_QUEUE: "An error occurred while adding messages to the queue.",
        MessageKey.SLOTS_GAME_MENU: """Welcome to the slots section.\nHere you can win a lot of money, here are the winning combinations:\n1. 🦎🦎🦎 - x10\n2.  🏜️🏜️🏜️ - x5\n3. 🏖️🏖️🏖️ - x3\n4. 🏕️🏕️🏕️ - x2\n5. ✈️✈️✈️ - x1.8\n6. 🚀🚀🚀 - x1.7\n7. 🪲🪲🪲 - x1.5\n8. 🐞🐞🐞 - x1.2\n9. 🐝🐝🐝 - x1.05\nGood luck! You will need it.\nHow much $GMEME are we playing for?""",
        MessageKey.SLOTS_NOT_ENOUGH_TO_PLAY: "💲You don't have enough balance to play. Try changing the amount.",
        MessageKey.SLOTS_WIN: "🎉Congratulations, you won: {amount} $GMEME\n🎰Your winning combination: {combination}",
        MessageKey.SLOTS_LOSS: "🃏Unfortunately, this time you lost your bet ({amount} $GMEME).\n🎰Your combination: {combination}\nTry again, luck will surely be on your side!",
        MessageKey.ADMIN_TASK_MENU: "📋Select your action",
        MessageKey.ADMIN_TASK_TYPE_SELECT: "Select the task type",
        MessageKey.ADMIN_TASK_TITLE_REQUEST: "Enter the task title:",
        MessageKey.ADMIN_TASK_TEXT_REQUEST: "Enter the task text:",
        MessageKey.ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST: "Enter the chat_id of channels, groups, separated by commas.",
        MessageKey.ADMIN_TASK_EXPIRE_TIME_REQUEST: "Enter the task expiration time.\nexample: 10h",
        MessageKey.ADMIN_TASK_GMEME_DONE_REWARD_REQUEST: "Enter the reward amount in $GMEME.",
        MessageKey.ADMIN_TASK_BMEME_DONE_REWARD_REQUEST: "Enter the reward amount in $BMEME.",
        MessageKey.TIME_BASED_TASK: "<b>{title}</b>\n\nid: {task_id}\nDescription: {text}\nReward: {done_reward} $GMEME\nTime left: {expires_in}",
        MessageKey.BONUS_TASK: "<b>{title}</b>\n\nDescription:\n{text}\nPayment: {done_reward} $GMEME",
        MessageKey.ADMIN_TASK_SAVED_SUCCESSFULLY: "Task with id: {task_id} was saved successfully",
        MessageKey.ADMIN_TASK_ID_REQUEST: "Enter the task id:",
        MessageKey.ADMIN_CONFIRM_TASK_DELETE: "^^^- delete this task?",
        MessageKey.ADMIN_TASK_DELETED_SUCCESSFULLY: "Task deleted successfully!",
        MessageKey.CHOOSE_TASK_TYPE: "🔥 In our bot, you can earn by completing our tasks!",
        MessageKey.CHOOSE_BONUS: "🎁 Choose the bonus task you want to complete:",
        MessageKey.TASK_ENDED: "😞 No tasks left! Please try again later.",
        MessageKey.BONUS_TASK_ENDED: "😞 Unfortunately, there are no bonus tasks available for you at the moment. Please try again later.",
        MessageKey.TASK_DONE_SUCCESSFULLY: "✅ You have successfully completed task №{task_id}",
        MessageKey.TASK_DONE_UNSUCCESSFULLY: "❌ You did not meet the task requirements!",
        MessageKey.TASK_ALREADY_HAS_DONE: "❌ You have already completed this task!",
        MessageKey.PUBLIC_STATISTIC: "📊 <b>Project Statistics:</b>\n\n👥 Total users: {total_users}\n👤 New today: {today_joined}",
    },
    Lang.TR: {
        MessageKey.LANG_CHANGE: "Dil başarıyla Türkçe olarak değiştirildi!",
        MessageKey.START_REQUIRE_SUBSCRIPTION: "<b>🦎 Devam etmek için kanallarımıza abone olmanız gerekiyor:</b>",
        MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL: "✅ Başarıyla abone oldunuz!",
        MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED: "⛔️ Kanallarımıza abone olun ve tekrar deneyin!",
        MessageKey.MENU_MESSAGE: "<b>🦎 Bu botta şunları yapabilirsiniz:</b>",
        MessageKey.REF_INVITED_STEP_ONE: "👥 <a href=\"tg://user?id={user_link}\">Bir arkadaşınızı</a> davet ettiniz! Arkadaşınız kanallara abone olduğunda {amount} $GMEME kazanacaksınız!",
        MessageKey.REF_INVITED_STEP_TWO: "👥 <a href=\"tg://user?id={user_link}\">Arkadaşınızın</a> botta kaydı için {amount} $GMEME kazandınız",
        MessageKey.REF_INVITE: """👥 Arkadaşlarını davet et ve kişi başına {ref_invite_pay} $GMEME kazan\n\n🔗 Bağlantınız: <code>https://t.me/Geckoshi_bot?start={link}</code>\n\n🗣 Toplamda: {ref_invite_count} kişi davet ettiniz""",
        MessageKey.USER_PROFILE: """📝 Ad: <a href=\"tg://user?id={user_link}\">{user_name}</a>\n🆔 Kimlik Numaranız: <code>{user_tg_id}</code>\n🔥 Premium hesap: {is_premium_account}\n💎 Bakiye: {balance} $GMEME\n👥 Toplam referans: {ref_count}\n🦎 ÇEKİLDİ: {withdrew} $GMEME\n<b>📣 Ödemeler hakkında önceden bilgi vereceğiz!\n🔥 Haberleri takip edin!\n⛔️ EN DÜŞÜK ÇEKİM MİKTARI, AIRDROP GÜNÜ {min_withdraw_in_airdrop} OLACAKTIR!</b>""",
        MessageKey.LANG_MENU: "Tercih ettiğiniz dili seçin:",
        MessageKey.FUNCTION_NOT_IMPLEMENTED: "Ne yazık ki bu özellik şu anda mevcut değil",
        MessageKey.PREMIUM_ALREADY_BOUGHT: "❗ Zaten Premium'a sahipsiniz!",
        MessageKey.PREMIUM_BUY_MENU: "🦎 Premium fiyatı: {premium_gmeme_price} $GMEME",
        MessageKey.NOT_ENOUGH_TO_BUY_PREMIUM: "❗ Premium satın almak için yeterli {not_enough} $GMEME'niz yok",
        MessageKey.PREMIUM_HAS_BOUGHT: "🥳 'Premium' satın aldınız",
        MessageKey.SOON: "Yakında 🔜",
        MessageKey.ADMIN_PANEL: "Yönetim Paneli:\n\n🕰Bot Çalışma Süresi: {uptime}\n👥Bottaki kullanıcı sayısı: {user_count}",
        MessageKey.ADMIN_NOW: "Yönetici hakları verildi",
        MessageKey.ADMIN_CHANGE_REF_PAY: "Referans ödülü için yeni miktarı girin.\nMevcut değer: {pay_for_ref}",
        MessageKey.ADMIN_CHANGE_REF_PAY_SUCCESSFULLY: "Referans ödülü miktarı şu şekilde değiştirildi: {pay_for_ref}",
        MessageKey.ADMIN_ENTER_MAILING_MESSAGE: "Gönderim için metin girin veya bir resim gönderin:",
        MessageKey.ADMIN_MAILING_HAS_INLINE_BUTTON: "Bir bağlantı içeren satır içi buton eklemek ister misiniz?",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_TEXT: "Satır içi buton için metin girin:",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_URL: "Satır içi buton için URL'yi girin:",
        MessageKey.ADMIN_ADD_INLINE_BUTTON: "Satır içi buton başarıyla eklendi!",
        MessageKey.ADMIN_INLINE_BUTTON_PREVIEW: "Buton şu şekilde görünecektir:",
        MessageKey.ADMIN_MAILING_MESSAGE_LOOKS_LIKE: "^^^ - gönderim mesajı böyle görünecek.",
        MessageKey.ADMIN_MAILING_STATS: "Gönderim İstatistikleri No.{mailing_id}:\n Yakalanan kullanıcılar: {user_captured}\n Durum: {status}\n Başarılı: {successfully}\n Kuyrukta: {in_queue}\n Başarısız: {failed}\n İptal Edildi: {canceled}\n Toplam işlenen: {messages_processed} ({messages_processed_percents})\n İşlem süresi: {processing_time}",
        MessageKey.REQUEST_PROCESSING: "İstek işleniyor...",
        MessageKey.ADMIN_MAILING_CANCEL_FAILED: "Gönderim iptal edilemedi.",
        MessageKey.ADMIN_MAILING_CANCEL_SUCCESSFUL: "Gönderim No.{mailing_id} başarıyla iptal edildi!",
        MessageKey.ADMIN_MAILING_FAILED_TO_SEND_MESSAGES_IN_QUEUE: "Kuyruğa mesaj eklerken bir hata oluştu.",
        MessageKey.SLOTS_GAME_MENU: """Slot bölümüne hoş geldiniz.\nBurada çok para kazanabilirsiniz, işte kazanan kombinasyonlar:\n1. 🦎🦎🦎 - x10\n2.  🏜️🏜️🏜️ - x5\n3. 🏖️🏖️🏖️ - x3\n4. 🏕️🏕️🏕️ - x2\n5. ✈️✈️✈️ - x1.8\n6. 🚀🚀🚀 - x1.7\n7. 🪲🪲🪲 - x1.5\n8. 🐞🐞🐞 - x1.2\n9. 🐝🐝🐝 - x1.05\nİyi şanslar! İhtiyacınız olacak.\nNe kadar $GMEME ile oynuyoruz?""",
        MessageKey.SLOTS_NOT_ENOUGH_TO_PLAY: "💲Oynamak için yeterli bakiyeniz yok. Miktarı değiştirmeyi deneyin.",
        MessageKey.SLOTS_WIN: "🎉Tebrikler, kazandınız: {amount} $GMEME\n🎰Kazanan kombinasyonunuz: {combination}",
        MessageKey.SLOTS_LOSS: "🃏Maalesef bu sefer bahsinizi kaybettiniz ({amount} $GMEME).\n🎰Kombinasyonunuz: {combination}\nTekrar deneyin, şans size gülecektir!",
        MessageKey.ADMIN_TASK_MENU: "📋Eyleminizi seçin",
        MessageKey.ADMIN_TASK_TYPE_SELECT: "Görev türünü seçin",
        MessageKey.ADMIN_TASK_TITLE_REQUEST: "Görevin başlığını girin:",
        MessageKey.ADMIN_TASK_TEXT_REQUEST: "Görevin metnini girin:",
        MessageKey.ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST: "Virgülle ayrılmış kanal, grup chat_id'lerini girin.",
        MessageKey.ADMIN_TASK_EXPIRE_TIME_REQUEST: "Görevin süresini girin.\nörnek: 10h",
        MessageKey.ADMIN_TASK_GMEME_DONE_REWARD_REQUEST: "$GMEME olarak ödül miktarını girin.",
        MessageKey.ADMIN_TASK_BMEME_DONE_REWARD_REQUEST: "$BMEME olarak ödül miktarını girin.",
        MessageKey.TIME_BASED_TASK: "<b>{title}</b>\n\nid: {task_id}\nAçıklama: {text}\nÖdül: {done_reward} $GMEME\nKalan zaman: {expires_in}",
        MessageKey.BONUS_TASK: "<b>{title}</b>\n\nAçıklama:\n{text}\nÖdeme: {done_reward} $GMEME",
        MessageKey.ADMIN_TASK_SAVED_SUCCESSFULLY: "Görev id'si ile: {task_id} başarıyla kaydedildi",
        MessageKey.ADMIN_TASK_ID_REQUEST: "Görev kimliğini girin:",
        MessageKey.ADMIN_CONFIRM_TASK_DELETE: "^^^- bu görevi silmek istiyor musunuz?",
        MessageKey.ADMIN_TASK_DELETED_SUCCESSFULLY: "Görev başarıyla silindi!",
        MessageKey.CHOOSE_TASK_TYPE: "🔥 Botumuzda görev yaparak para kazanabilirsiniz!",
        MessageKey.CHOOSE_BONUS: "🎁 Tamamlamak istediğiniz bonus görevi seçin:",
        MessageKey.TASK_ENDED: "😞 Maalesef, şu anda sizin için uygun bonus görev yok. Lütfen daha sonra tekrar deneyin.",
        MessageKey.BONUS_TASK_ENDED: "😞 К сожаленю, сейчас нет бонусных заданий для вас. Попробуйте позднее.",
        MessageKey.TASK_DONE_SUCCESSFULLY: "✅ Görevi başarıyla tamamladınız №{task_id}",
        MessageKey.TASK_DONE_UNSUCCESSFULLY: "❌ Görevin gerekliliklerini yerine getirmediniz!",
        MessageKey.TASK_ALREADY_HAS_DONE: "❌ Bu görevi zaten tamamladınız!",
        MessageKey.PUBLIC_STATISTIC: "📊 <b>Proje İstatistikleri:</b>\n\n👥 Toplam kullanıcı: {total_users}\n👤 Bugün eklenenler: {today_joined}",

    },
    Lang.DE: {
        MessageKey.LANG_CHANGE: "Die Sprache wurde erfolgreich auf Deutsch geändert!",
        MessageKey.START_REQUIRE_SUBSCRIPTION: "<b>🦎 Um fortzufahren, müssen Sie unsere Kanäle abonniert haben:</b>",
        MessageKey.START_REQUIRE_SUBSCRIPTION_SUCCESSFUL: "✅ Sie haben erfolgreich abonniert!",
        MessageKey.START_REQUIRE_SUBSCRIPTION_FAILED: "⛔️ Bitte abonnieren Sie unsere Kanäle und versuchen Sie es erneut!",
        MessageKey.MENU_MESSAGE: "<b>🦎 In diesem Bot können Sie:</b>",
        MessageKey.REF_INVITED_STEP_ONE: "👥 Sie haben <a href=\"tg://user?id={user_link}\">einen Freund!</a> eingeladen! Sie erhalten {amount} $GMEME, sobald Ihr Freund die Kanäle abonniert hat!",
        MessageKey.REF_INVITED_STEP_TWO: "👥 Sie haben {amount} $GMEME für die Registrierung Ihres <a href=\"tg://user?id={user_link}\">Freundes</a> im Bot erhalten",
        MessageKey.REF_INVITE: """👥 Laden Sie Freunde ein und verdienen Sie jeweils {ref_invite_pay} $GMEME\n\n🔗 Ihr Link: <code>https://t.me/Geckoshi_bot?start={link}</code>\n\n🗣 Sie haben insgesamt: {ref_invite_count} Personen eingeladen""",
        MessageKey.USER_PROFILE: """📝 Name: <a href=\"tg://user?id={user_link}\">{user_name}</a>\n🆔 Ihre ID: <code>{user_tg_id}</code>\n🔥 Premium-Konto: {is_premium_account}\n💎 Guthaben: {balance} $GMEME\n👥 Gesamtanzahl der Empfehlungen: {ref_count}\n🦎 AUSGEZAHLT: {withdrew} $GMEME\n<b>📣 Wir werden Sie im Voraus über Auszahlungen informieren!\n🔥 Bleiben Sie auf dem Laufenden!\n⛔️ MINDESTABHEBUNG WIRD {min_withdraw_in_airdrop} AM TAG DES AIRDROPS SEIN!</b>""",
        MessageKey.LANG_MENU: "Wählen Sie Ihre bevorzugte Sprache:",
        MessageKey.FUNCTION_NOT_IMPLEMENTED: "Leider ist diese Funktion derzeit nicht verfügbar",
        MessageKey.PREMIUM_ALREADY_BOUGHT: "❗ Sie haben bereits Premium!",
        MessageKey.PREMIUM_BUY_MENU: "🦎 Premium-Preis: {premium_gmeme_price} $GMEME",
        MessageKey.NOT_ENOUGH_TO_BUY_PREMIUM: "❗ Sie haben nicht genug {not_enough} $GMEME, um Premium zu kaufen",
        MessageKey.PREMIUM_HAS_BOUGHT: "🥳 Sie haben 'Premium' gekauft",
        MessageKey.SOON: "Bald verfügbar 🔜",
        MessageKey.ADMIN_PANEL: "Admin-Panel:\n\n🕰Bot-Laufzeit: {uptime}\n👥Nutzer im Bot: {user_count}",
        MessageKey.ADMIN_NOW: "Ihnen wurden Administratorrechte erteilt",
        MessageKey.ADMIN_CHANGE_REF_PAY: "Geben Sie den neuen Betrag für die Empfehlungsbelohnung ein.\nAktueller Wert: {pay_for_ref}",
        MessageKey.ADMIN_CHANGE_REF_PAY_SUCCESSFULLY: "Die Empfehlungsbelohnung wurde auf: {pay_for_ref} geändert",
        MessageKey.ADMIN_ENTER_MAILING_MESSAGE: "Geben Sie den Text für die Mailing-Nachricht ein oder senden Sie ein Bild:",
        MessageKey.ADMIN_MAILING_HAS_INLINE_BUTTON: "Möchten Sie einen Inline-Button mit einem Link hinzufügen?",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_TEXT: "Geben Sie den Text für den Inline-Button ein:",
        MessageKey.ADMIN_ENTER_INLINE_BUTTON_URL: "Geben Sie die URL für den Inline-Button ein:",
        MessageKey.ADMIN_ADD_INLINE_BUTTON: "Inline-Button erfolgreich hinzugefügt!",
        MessageKey.ADMIN_INLINE_BUTTON_PREVIEW: "Der Button wird wie folgt aussehen:",
        MessageKey.ADMIN_MAILING_MESSAGE_LOOKS_LIKE: "^^^ - so wird die Mailing-Nachricht aussehen.",
        MessageKey.ADMIN_MAILING_STATS: "Mailing-Statistiken Nr.{mailing_id}:\n Erreichte Nutzer: {user_captured}\n Status: {status}\n Erfolgreich: {successfully}\n In der Warteschlange: {in_queue}\n Fehlgeschlagen: {failed}\n Abgebrochen: {canceled}\n Insgesamt verarbeitet: {messages_processed} ({messages_processed_percents})\n Bearbeitungszeit: {processing_time}",
        MessageKey.REQUEST_PROCESSING: "Anfrage wird verarbeitet...",
        MessageKey.ADMIN_MAILING_CANCEL_FAILED: "Das Mailing konnte nicht abgebrochen werden.",
        MessageKey.ADMIN_MAILING_CANCEL_SUCCESSFUL: "Mailing Nr.{mailing_id} erfolgreich abgebrochen!",
        MessageKey.ADMIN_MAILING_FAILED_TO_SEND_MESSAGES_IN_QUEUE: "Ein Fehler ist aufgetreten, als Nachrichten zur Warteschlange hinzugefügt wurden.",
        MessageKey.SLOTS_GAME_MENU: """Willkommen im Slot-Bereich.\nHier können Sie viel Geld gewinnen, hier sind die Gewinnkombinationen:\n1. 🦎🦎🦎 - x10\n2.  🏜️🏜️🏜️ - x5\n3. 🏖️🏖️🏖️ - x3\n4. 🏕️🏕️🏕️ - x2\n5. ✈️✈️✈️ - x1.8\n6. 🚀🚀🚀 - x1.7\n7. 🪲🪲🪲 - x1.5\n8. 🐞🐞🐞 - x1.2\n9. 🐝🐝🐝 - x1.05\nViel Glück! Sie werden es brauchen.\nFür wie viel $GMEME spielen wir?""",
        MessageKey.SLOTS_NOT_ENOUGH_TO_PLAY: "💲Sie haben nicht genug Guthaben, um zu spielen. Versuchen Sie, den Betrag zu ändern.",
        MessageKey.SLOTS_WIN: "🎉Herzlichen Glückwunsch, Sie haben gewonnen: {amount} $GMEME\n🎰Ihre Gewinnkombination: {combination}",
        MessageKey.SLOTS_LOSS: "🃏Leider haben Sie diesmal Ihren Einsatz verloren ({amount} $GMEME).\n🎰Ihre Kombination: {combination}\nVersuchen Sie es erneut, das Glück wird sicherlich auf Ihrer Seite sein!",
        MessageKey.ADMIN_TASK_MENU: "📋Wählen Sie Ihre Aktion",
        MessageKey.ADMIN_TASK_TYPE_SELECT: "Wählen Sie den Aufgabentyp",
        MessageKey.ADMIN_TASK_TITLE_REQUEST: "Geben Sie den Titel der Aufgabe ein:",
        MessageKey.ADMIN_TASK_TEXT_REQUEST: "Geben Sie den Text der Aufgabe ein:",
        MessageKey.ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST: "Geben Sie die chat_id von Kanälen, Gruppen, durch Kommas getrennt, ein.",
        MessageKey.ADMIN_TASK_EXPIRE_TIME_REQUEST: "Geben Sie die Ablaufzeit der Aufgabe ein.\nBeispiel: 10h",
        MessageKey.ADMIN_TASK_GMEME_DONE_REWARD_REQUEST: "Geben Sie die Belohnungssumme in $GMEME ein.",
        MessageKey.ADMIN_TASK_BMEME_DONE_REWARD_REQUEST: "Geben Sie die Belohnungssumme in $BMEME ein.",
        MessageKey.TIME_BASED_TASK: "<b>{title}</b>\n\nid: {task_id}\nBeschreibung: {text}\nBelohnung: {done_reward} $GMEME\nVerbleibende Zeit: {expires_in}",
        MessageKey.BONUS_TASK: "<b>{title}</b>\n\nBeschreibung:\n{text}\nBezahlung: {done_reward} $GMEME",
        MessageKey.ADMIN_TASK_SAVED_SUCCESSFULLY: "Aufgabe mit der id: {task_id} wurde erfolgreich gespeichert",
        MessageKey.ADMIN_TASK_ID_REQUEST: "Geben Sie die Aufgaben-ID ein:",
        MessageKey.ADMIN_CONFIRM_TASK_DELETE: "^^^- diese Aufgabe löschen?",
        MessageKey.ADMIN_TASK_DELETED_SUCCESSFULLY: "Aufgabe erfolgreich gelöscht!",
        MessageKey.CHOOSE_TASK_TYPE: "🔥 In unserem Bot können Sie durch das Erledigen von Aufgaben verdienen!",
        MessageKey.CHOOSE_BONUS: "🎁 Wählen Sie die Bonusaufgabe, die Sie erledigen möchten:",
        MessageKey.TASK_ENDED: "😞 Keine Aufgaben mehr! Versuchen Sie es später erneut.",
        MessageKey.BONUS_TASK_ENDED: "😞 Leider gibt es momentan keine Bonustasks für Sie. Bitte versuchen Sie es später erneut.",
        MessageKey.TASK_DONE_SUCCESSFULLY: "✅ Sie haben die Aufgabe №{task_id} erfolgreich abgeschlossen",
        MessageKey.TASK_DONE_UNSUCCESSFULLY: "❌ Sie haben die Anforderungen der Aufgabe nicht erfüllt!",
        MessageKey.TASK_ALREADY_HAS_DONE: "❌ Sie haben diese Aufgabe bereits abgeschlossen!",
        MessageKey.PUBLIC_STATISTIC: "📊 <b>Projektstatistik:</b>\n\n👥 Gesamtanzahl der Benutzer: {total_users}\n👤 Neu heute: {today_joined}",
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
        [
            M(text="🎁 bonus", callback_class=StartCreatingTask, with_callback_param_required=True),
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
    KeyboardKey.BONUS_TASK_BUTTON: [
        [
            M(text="{title}", callback_class=BonusTaskSelect, with_callback_param_required=True, with_text_param_required=True),
        ],
    ],
    Lang.RU: {
        KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB: [
            [
                M(id_="@geckoshi_coin", text="1️⃣ Подписка №1", url="https://t.me/geckoshi_coin"),
                M(id_="@geckoshichat", text="2️⃣ Подписка №2", url="https://t.me/geckoshichat"),
            ],
            [
                M(text="3️⃣ Подписка №3", url="https://twitter.com/geckoshi_coin"),
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
            [
                M(text="📈 Buy/Sell BMEME", url="https://dedust.io/swap/TON/EQBMLARhzX35GDwjHeWwUMuZ5Oz65z1Tk0XodZBI8qxNllRu?amount=1000000000"),
            ],
        ],
        KeyboardKey.REF_LINK_SHARE: [
            [
                M(text="🔗 Выслать приглашение", url="https://t.me/share/url?url=https://t.me/Geckoshi_bot?start={ref_link}", with_url_placeholder=True)
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
        KeyboardKey.SELECT_TASK_SUBMIT_BUTTON: [
            [
                M(text="✅ Проверить", callback_class=TaskDone, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SELECT_TASK_NAV_MENU: [
            [
                M(text="⬅️ Предыдущее", callback_class=TaskSelect, with_callback_param_required=True),
                M(text="Следующее ➡️", callback_class=TaskSelect, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.PAGINATION_MENU: [
            [
                M(text="⬅️", callback_class=PaginationMove, with_callback_param_required=True),
                M(text="{cur_page}/{total_pages}", callback_class=Void, with_text_param_required=True),
                M(text="➡️", callback_class=PaginationMove, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SKIP: [
            [
                M(text="Пропустить ⤵️", callback_class=Skip),
            ],
        ],
    },
    Lang.EN: {
        KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB: [
            [
                M(id_="@geckoshi_coin", text="1️⃣ Subscription #1", url="https://t.me/geckoshi_coin"),
                M(id_="@geckoshichat", text="2️⃣ Subscription #2", url="https://t.me/geckoshichat"),
            ],
            [
                M(text="3️⃣ Subscription #3", url="https://twitter.com/geckoshi_coin"),
            ],
            [
                M(text="✅ Subscribed", callback_class=CheckStartMembershipCallback)
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
                M(text="💸 Earn", callback_class=MenuToRefCallback),
                M(text="🎁 Bonus", callback_class=MenuToBonusCallback),
            ],
            [
                M(text="📣 Tasks", callback_class=MenuToTasksCallback),
                M(text="🏷 Cheques", callback_class=MenuToChequeCallback),
            ],
            [
                M(text="🗳 P2P", callback_class=MenuToP2PCallback),
                M(text="🎰 Slots", callback_class=MenuToSlotsCallback),
            ],
            [
                M(text="🧩 NFT", callback_class=MenuToNFTCallback),
                M(text="💼 Profile", callback_class=MenuToProfileCallback),
            ],
            [
                M(text="📊 Statistics", callback_class=MenuToStatistic),
            ],
            [
                M(text="📈 Buy/Sell BMEME", url="https://dedust.io/swap/TON/EQBMLARhzX35GDwjHeWwUMuZ5Oz65z1Tk0XodZBI8qxNllRu?amount=1000000000"),
            ],
        ],
        KeyboardKey.REF_LINK_SHARE: [
            [
                M(text="🔗 Send Invitation", url="https://t.me/share/url?url=https://t.me/Geckoshi_bot?start={ref_link}", with_url_placeholder=True)
            ]
        ],
        KeyboardKey.PROFILE: [
            [
                M(text="📤 Withdraw", callback_class=ProfileWithdraw),
                M(text="🔥 Premium", callback_class=BuyPremiumMenu)
            ],
            [
                M(text="🎟 Activate Promo Code", callback_class=ActivateVoucher)
            ],
            [
                M(text="🔄 Change Language", callback_class=SetLangMenu)
            ],
        ],
        KeyboardKey.EXIT: [
            [
                M(text="❌ Exit", callback_class=Exit)
            ]
        ],
        KeyboardKey.STEP_BACK: [
            [
                M(text="⬅️ Back", callback_class=StepBack)
            ]
        ],
        KeyboardKey.BUY_PREMIUM_MENU: [
            [
                M(text="🔥 Buy Premium", callback_class=BuyPremium)
            ]
        ],
        KeyboardKey.ADMIN_PANEL: [
            [
                M(text="✉️ Mailing", callback_class=MailingCallback),
                M(text="🔎 Management", callback_class=UserManagement),
            ],
            [
                M(text="👥 Top Referrals", callback_class=RefTop, with_callback_param_required=True),
                M(text="This Week", callback_class=RefTop, with_callback_param_required=True),
                M(text="👥 Referral Payment", callback_class=ChangeRefPay),
            ],
            [
                M(text="🦎 Create Promo Code", callback_class=CreateVoucher),
                M(text="📝 Task", callback_class=TaskMenu),
            ],
        ],
        KeyboardKey.YES_NO: [
            [
                M(text="Yes", callback_class=Yes),
                M(text="No", callback_class=No)
            ]
        ],
        KeyboardKey.ADMIN_ADD_BUTTON_OR_PREVIEW: [
            [
                M(text="Add More Button", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Preview Message", callback_class=MailingMessagePreview),
            ],
        ],
        KeyboardKey.ADMIN_ADD_MORE_BUTTONS_OR_CONTINUE: [
            [
                M(text="Add More Button", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Continue", callback_class=Continue),
            ],
        ],
        KeyboardKey.ADMIN_INLINE_BUTTON_PREVIEW: [
            [
                M(text="Add", callback_class=ApproveInlineButton),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_START: [
            [
                M(text="Start Mailing", callback_class=StartMailing),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_MENU: [
            [
                M(text="Cancel Mailing", callback_class=StopMailing, with_callback_param_required=True),
                M(text="Update", callback_class=UpdateMailingStatistic, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_QUEUE_FILL_RETRY: [
            [
                M(text="Retry", callback_class=QueueFillMailingRetry, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SLOTS_CONTINUE_PLAY: [
            [
                M(text="Repeat Bet", callback_class=SlotsPlay, with_callback_param_required=True),
            ],
            [
                M(text="Change Bet", callback_class=InlineKeyboardChange),
            ],
        ],
        KeyboardKey.BACK_TO_MENU: [
            [
                M(text="❌ Back to Menu", callback_class=BackToMenu, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.TASK_MENU: [
            [
                M(text="Create", callback_class=CreateTask),
                M(text="Delete", callback_class=DeleteTaskMenu),
            ],
        ],
        KeyboardKey.CONTINUE_OR_RETRY: [
            [
                M(text="Continue", callback_class=Continue),
                M(text="Retry", callback_class=Retry),
            ],
        ],
        KeyboardKey.SAVE: [
            [
                M(text="Save", callback_class=Save),
            ],
        ],
        KeyboardKey.DELETE_TASK_MENU: [
            [
                M(text="Delete", callback_class=DeleteTask, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SELECT_TASK_NAV_MENU: [
            [
                M(text="✅ Check", callback_class=TaskDone, with_callback_param_required=True),
            ],
            [
                M(text="⬅️ Previous", callback_class=TaskSelect, with_callback_param_required=True),
                M(text="Next ➡️", callback_class=TaskSelect, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SKIP: [
            [
                M(text="Skip ⤵️", callback_class=Skip),
            ],
        ],
    },
    Lang.TR: {
        KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB: [
            [
                M(id_="@geckoshi_coin", text="1️⃣ Abonelik #1", url="https://t.me/geckoshi_coin"),
                M(id_="@geckoshichat", text="2️⃣ Abonelik #2", url="https://t.me/geckoshichat"),
            ],
            [
                M(text="3️⃣ Abonelik #3", url="https://twitter.com/geckoshi_coin"),
            ],
            [
                M(text="✅ Abone Oldum", callback_class=CheckStartMembershipCallback)
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
                M(text="💸 Kazan", callback_class=MenuToRefCallback),
                M(text="🎁 Bonus", callback_class=MenuToBonusCallback),
            ],
            [
                M(text="📣 Görevler", callback_class=MenuToTasksCallback),
                M(text="🏷 Çekler", callback_class=MenuToChequeCallback),
            ],
            [
                M(text="🗳 P2P", callback_class=MenuToP2PCallback),
                M(text="🎰 Slotlar", callback_class=MenuToSlotsCallback),
            ],
            [
                M(text="🧩 NFT", callback_class=MenuToNFTCallback),
                M(text="💼 Profil", callback_class=MenuToProfileCallback),
            ],
            [
                M(text="📊 İstatistikler", callback_class=MenuToStatistic),
            ],
            [
                M(text="📈 Buy/Sell BMEME", url="https://dedust.io/swap/TON/EQBMLARhzX35GDwjHeWwUMuZ5Oz65z1Tk0XodZBI8qxNllRu?amount=1000000000"),
            ],
        ],
        KeyboardKey.REF_LINK_SHARE: [
            [
                M(text="🔗 Davet Gönder", url="https://t.me/share/url?url=https://t.me/Geckoshi_bot?start={ref_link}", with_url_placeholder=True)
            ]
        ],
        KeyboardKey.PROFILE: [
            [
                M(text="📤 Çekil", callback_class=ProfileWithdraw),
                M(text="🔥 Premium", callback_class=BuyPremiumMenu)
            ],
            [
                M(text="🎟 Promosyon Kodunu Aktifleştir", callback_class=ActivateVoucher)
            ],
            [
                M(text="🔄 Dili Değiştir", callback_class=SetLangMenu)
            ],
        ],
        KeyboardKey.EXIT: [
            [
                M(text="❌ Çıkış", callback_class=Exit)
            ]
        ],
        KeyboardKey.STEP_BACK: [
            [
                M(text="⬅️ Geri", callback_class=StepBack)
            ]
        ],
        KeyboardKey.BUY_PREMIUM_MENU: [
            [
                M(text="🔥 Premium Satın Al", callback_class=BuyPremium)
            ]
        ],
        KeyboardKey.ADMIN_PANEL: [
            [
                M(text="✉️ Posta", callback_class=MailingCallback),
                M(text="🔎 Yönetim", callback_class=UserManagement),
            ],
            [
                M(text="👥 En İyi Referanslar", callback_class=RefTop, with_callback_param_required=True),
                M(text="Bu Hafta", callback_class=RefTop, with_callback_param_required=True),
                M(text="👥 Referans Ücreti", callback_class=ChangeRefPay),
            ],
            [
                M(text="🦎 Promosyon Kodu Oluştur", callback_class=CreateVoucher),
                M(text="📝 Görev", callback_class=TaskMenu),
            ],
        ],
        KeyboardKey.YES_NO: [
            [
                M(text="Evet", callback_class=Yes),
                M(text="Hayır", callback_class=No)
            ]
        ],
        KeyboardKey.ADMIN_ADD_BUTTON_OR_PREVIEW: [
            [
                M(text="Daha Fazla Buton Ekle", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Mesajı Önizle", callback_class=MailingMessagePreview),
            ],
        ],
        KeyboardKey.ADMIN_ADD_MORE_BUTTONS_OR_CONTINUE: [
            [
                M(text="Daha Fazla Buton Ekle", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Devam Et", callback_class=Continue),
            ],
        ],
        KeyboardKey.ADMIN_INLINE_BUTTON_PREVIEW: [
            [
                M(text="Ekle", callback_class=ApproveInlineButton),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_START: [
            [
                M(text="Posta Gönder", callback_class=StartMailing),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_MENU: [
            [
                M(text="Postayı İptal Et", callback_class=StopMailing, with_callback_param_required=True),
                M(text="Güncelle", callback_class=UpdateMailingStatistic, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_QUEUE_FILL_RETRY: [
            [
                M(text="Tekrar Dene", callback_class=QueueFillMailingRetry, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SLOTS_CONTINUE_PLAY: [
            [
                M(text="Bahsi Tekrarla", callback_class=SlotsPlay, with_callback_param_required=True),
            ],
            [
                M(text="Bahsi Değiştir", callback_class=InlineKeyboardChange),
            ],
        ],
        KeyboardKey.BACK_TO_MENU: [
            [
                M(text="❌ Menüye Dön", callback_class=BackToMenu, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.TASK_MENU: [
            [
                M(text="Oluştur", callback_class=CreateTask),
                M(text="Sil", callback_class=DeleteTaskMenu),
            ],
        ],
        KeyboardKey.CONTINUE_OR_RETRY: [
            [
                M(text="Devam Et", callback_class=Continue),
                M(text="Tekrar Dene", callback_class=Retry),
            ],
        ],
        KeyboardKey.SAVE: [
            [
                M(text="Kaydet", callback_class=Save),
            ],
        ],
        KeyboardKey.DELETE_TASK_MENU: [
            [
                M(text="Sil", callback_class=DeleteTask, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SELECT_TASK_NAV_MENU: [
            [
                M(text="✅ Kontrol Et", callback_class=TaskDone, with_callback_param_required=True),
            ],
            [
                M(text="⬅️ Önceki", callback_class=TaskSelect, with_callback_param_required=True),
                M(text="Sonraki ➡️", callback_class=TaskSelect, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SKIP: [
            [
                M(text="Geç ⤵️", callback_class=Skip),
            ],
        ],
    },
    Lang.DE: {
        KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB: [
            [
                M(id_="@geckoshi_coin", text="1️⃣ Abonnement #1", url="https://t.me/geckoshi_coin"),
                M(id_="@geckoshichat", text="2️⃣ Abonnement #2", url="https://t.me/geckoshichat"),
            ],
            [
                M(text="3️⃣ Abonnement #3", url="https://twitter.com/geckoshi_coin"),
            ],
            [
                M(text="✅ Abonniert", callback_class=CheckStartMembershipCallback)
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
                M(text="💸 Verdienen", callback_class=MenuToRefCallback),
                M(text="🎁 Bonus", callback_class=MenuToBonusCallback),
            ],
            [
                M(text="📣 Aufgaben", callback_class=MenuToTasksCallback),
                M(text="🏷 Schecks", callback_class=MenuToChequeCallback),
            ],
            [
                M(text="🗳 P2P", callback_class=MenuToP2PCallback),
                M(text="🎰 Slots", callback_class=MenuToSlotsCallback),
            ],
            [
                M(text="🧩 NFT", callback_class=MenuToNFTCallback),
                M(text="💼 Profil", callback_class=MenuToProfileCallback),
            ],
            [
                M(text="📊 Statistiken", callback_class=MenuToStatistic),
            ],
            [
                M(text="📈 Buy/Sell BMEME", url="https://dedust.io/swap/TON/EQBMLARhzX35GDwjHeWwUMuZ5Oz65z1Tk0XodZBI8qxNllRu?amount=1000000000"),
            ],
        ],
        KeyboardKey.REF_LINK_SHARE: [
            [
                M(text="🔗 Einladung Senden", url="https://t.me/share/url?url=https://t.me/Geckoshi_bot?start={ref_link}", with_url_placeholder=True)
            ]
        ],
        KeyboardKey.PROFILE: [
            [
                M(text="📤 Auszahlen", callback_class=ProfileWithdraw),
                M(text="🔥 Premium", callback_class=BuyPremiumMenu)
            ],
            [
                M(text="🎟 Promo-Code Aktivieren", callback_class=ActivateVoucher)
            ],
            [
                M(text="🔄 Sprache Ändern", callback_class=SetLangMenu)
            ],
        ],
        KeyboardKey.EXIT: [
            [
                M(text="❌ Aussteigen", callback_class=Exit)
            ]
        ],
        KeyboardKey.STEP_BACK: [
            [
                M(text="⬅️ Zurück", callback_class=StepBack)
            ]
        ],
        KeyboardKey.BUY_PREMIUM_MENU: [
            [
                M(text="🔥 Premium Kaufen", callback_class=BuyPremium)
            ]
        ],
        KeyboardKey.ADMIN_PANEL: [
            [
                M(text="✉️ Mailing", callback_class=MailingCallback),
                M(text="🔎 Verwaltung", callback_class=UserManagement),
            ],
            [
                M(text="👥 Top Referrals", callback_class=RefTop, with_callback_param_required=True),
                M(text="Diese Woche", callback_class=RefTop, with_callback_param_required=True),
                M(text="👥 Referral-Zahlung", callback_class=ChangeRefPay),
            ],
            [
                M(text="🦎 Promo-Code Erstellen", callback_class=CreateVoucher),
                M(text="📝 Aufgabe", callback_class=TaskMenu),
            ],
        ],
        KeyboardKey.YES_NO: [
            [
                M(text="Ja", callback_class=Yes),
                M(text="Nein", callback_class=No)
            ]
        ],
        KeyboardKey.ADMIN_ADD_BUTTON_OR_PREVIEW: [
            [
                M(text="Weitere Taste Hinzufügen", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Nachricht Vorschau", callback_class=MailingMessagePreview),
            ],
        ],
        KeyboardKey.ADMIN_ADD_MORE_BUTTONS_OR_CONTINUE: [
            [
                M(text="Weitere Taste Hinzufügen", callback_class=AddMoreInlineButton),
            ],
            [
                M(text="Fortsetzen", callback_class=Continue),
            ],
        ],
        KeyboardKey.ADMIN_INLINE_BUTTON_PREVIEW: [
            [
                M(text="Hinzufügen", callback_class=ApproveInlineButton),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_START: [
            [
                M(text="Mailing Starten", callback_class=StartMailing),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_MENU: [
            [
                M(text="Mailing Abbrechen", callback_class=StopMailing, with_callback_param_required=True),
                M(text="Aktualisieren", callback_class=UpdateMailingStatistic, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.ADMIN_MAILING_QUEUE_FILL_RETRY: [
            [
                M(text="Erneut Versuchen", callback_class=QueueFillMailingRetry, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SLOTS_CONTINUE_PLAY: [
            [
                M(text="Wette Wiederholen", callback_class=SlotsPlay, with_callback_param_required=True),
            ],
            [
                M(text="Wette Ändern", callback_class=InlineKeyboardChange),
            ],
        ],
        KeyboardKey.BACK_TO_MENU: [
            [
                M(text="❌ Zurück Zum Menü", callback_class=BackToMenu, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.TASK_MENU: [
            [
                M(text="Erstellen", callback_class=CreateTask),
                M(text="Löschen", callback_class=DeleteTaskMenu),
            ],
        ],
        KeyboardKey.CONTINUE_OR_RETRY: [
            [
                M(text="Fortsetzen", callback_class=Continue),
                M(text="Erneut Versuchen", callback_class=Retry),
            ],
        ],
        KeyboardKey.SAVE: [
            [
                M(text="Speichern", callback_class=Save),
            ],
        ],
        KeyboardKey.DELETE_TASK_MENU: [
            [
                M(text="Löschen", callback_class=DeleteTask, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SELECT_TASK_NAV_MENU: [
            [
                M(text="✅ Überprüfen", callback_class=TaskDone, with_callback_param_required=True),
            ],
            [
                M(text="⬅️ Vorherige", callback_class=TaskSelect, with_callback_param_required=True),
                M(text="Nächste ➡️", callback_class=TaskSelect, with_callback_param_required=True),
            ],
        ],
        KeyboardKey.SKIP: [
            [
                M(text="Überspringen ⤵️", callback_class=Skip),
            ],
        ],
    },
}
