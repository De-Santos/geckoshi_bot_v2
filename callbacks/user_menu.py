from aiogram.filters.callback_data import CallbackData


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

