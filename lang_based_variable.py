from enum import Enum
from typing import Any

from aiogram.filters.callback_data import CallbackData

KEYBOARD = "kb"
BOT_TG_URL = "https://t.me/Geckoshi_bot"


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


class KeyboardKey(Enum):
    START_REQUIRE_SUBSCRIPTION_KB = "start_required_subscription"
    MENU = "menu"
    ADMIN_MENU = "admin_menu"
    INLINE_MENU = "inline_menu"
    REF_LINK_SHARE = "ref_link_share"
    PROFILE = "profile"
    EXIT = "exit"
    BUY_PREMIUM_MENU = "buy_premium_menu"


class M:
    id_: str = None
    text: str
    url: str = None
    with_url_placeholder: bool = False
    callback_class: Any = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

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


class ActivatePromo(CallbackData, prefix="activate-promo"):
    pass


class SetLangMenu(CallbackData, prefix="set-lang-menu"):
    pass


class Exit(CallbackData, prefix="exit"):
    pass


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
        MessageKey.REF_INVITE: """👥 Приглашай друзей и получай по {ref_invite_pay} $GMEME\n\n🔗 Твоя ссылка: <code>https://t.me/TeestttgeckoshiBot?start={link}</code>\n\n🗣 Ты всего пригласил: {ref_invite_count} чел""",
        MessageKey.USER_PROFILE: """📝 Имя: <a href=\"tg://user?id={user_link}\">{user_name}</a>\n🆔 Ваш ID: <code>{user_tg_id}</code>\n🔥 Премиум аккаунт: {is_premium_account}\n💎 Баланс: {balance} $GMEME\n👥 Всего рефералов: {ref_count}\n🦎 ВЫВЕДЕНО: {withdrew} $GMEME\n<b>📣 Мы сообщим заранее о выплатах!\n🔥 Следите за новостями!\n⛔️ МИНИМАЛЬНЫЙ ВЫВОД БУДЕТ {min_withdraw_in_airdrop} В ДЕНЬ АИРДРОПА!</b>""",
        MessageKey.LANG_MENU: "Выберите желаемый язык:",
        MessageKey.FUNCTION_NOT_IMPLEMENTED: "К сожалению данная функция сейчас недоступна",
        MessageKey.PREMIUM_ALREADY_BOUGHT: "❗ У вас уже имеется Премиум!",
        MessageKey.PREMIUM_BUY_MENU: "🦎 Цена премиума: {premium_gmeme_price} $GMEME",
        MessageKey.NOT_ENOUGH_TO_BUY_PREMIUM: "❗ Для покупки не хватает {not_enough} $GMEME",
        MessageKey.PREMIUM_HAS_BOUGHT: "🥳 Вы приобрели \"Премиум\""
    },
}

keyboard_data = {
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
                M(text="🎟 Активировать промокод", callback_class=ActivatePromo)
            ],
            [
                M(text="🔄 Изменить язык", callback_class=SetLangMenu)
            ],
        ],
        KeyboardKey.EXIT: [
            [
                M(text="⬅️ Выйти", callback_class=Exit)
            ]
        ],
        KeyboardKey.BUY_PREMIUM_MENU: [
            [
                M(text="🔥 Купить премиум", callback_class=BuyPremium)
            ]
        ]
    }
}
