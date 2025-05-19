import logging
from aiogram import Bot
from config import CHANNELS_ID

async def check_all_channel_subscription(bot: Bot, user_id: int):
    for channel in CHANNELS_ID:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            logging.error(f"Error checking subscription: {e}")
            return False
    return True
