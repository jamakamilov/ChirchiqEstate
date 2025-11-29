from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import language_kb
from database import AsyncSessionLocal
from models.user import User
from utils.logger import logger
from config import settings

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    # send language selection
    await message.answer(settings.DEFAULT_LANGUAGE and "Welcome / Tilni tanlang" or "Welcome", reply_markup=language_kb())
    # create or update user
    async with AsyncSessionLocal() as session:
        q = await session.execute(
            __import__("sqlalchemy").select(User).where(User.telegram_id == message.from_user.id)
        )
        user = q.scalar_one_or_none()
        if not user:
            user = User(telegram_id=message.from_user.id, name=message.from_user.full_name)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logger.info(f"Created user {user.telegram_id}")
