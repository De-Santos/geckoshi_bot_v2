from api.public_api.dto import UserRegistrationInfo
from database import get_user_by_tg


async def get_user_register_info(user_id: int) -> UserRegistrationInfo:
    user = await get_user_by_tg(user_id)
    if user is None:
        return UserRegistrationInfo(exists=False)

    return UserRegistrationInfo(exists=True, registration_finished=True)
