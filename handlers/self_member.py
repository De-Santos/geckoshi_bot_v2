from aiogram import Router, types, Bot

router = Router(name="bot_router")


@router.my_chat_member()
async def handle_bot_added_to_chat(event: types.ChatMemberUpdated, bot: Bot):
    print(event)
    # if event.new_chat_member.user.id == bot.id:
    #     chat = event.chat
    #     if event.new_chat_member.status in ['member', 'administrator']:
    #         chat_type = chat.type
    #         chat_id = chat.id
    #         if chat_type == ChatType.GROUP or chat_type == ChatType.SUPERGROUP:
    #             logging.info(f"Bot added to group: {chat.title}, chat_id: {chat_id}")
    #             await bot.send_message(chat_id, "Hello! I've been added to this group.")
    #         elif chat_type == ChatType.CHANNEL:
    #             logging.info(f"Bot added to channel: {chat.title}, chat_id: {chat_id}")
