from aiogram import Bot
from config import settings
from utils.logger import logger

bot = Bot(token=settings.BOT_TOKEN)

async def notify_admins(text: str):
    admin_ids = [int(x) for x in settings.ADMIN_IDS.split(",") if x.strip()]
    for aid in admin_ids:
        try:
            await bot.send_message(aid, text)
        except Exception as e:
            logger.error(f"Failed to notify admin {aid}: {e}")
