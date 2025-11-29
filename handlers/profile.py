from aiogram import Router
from aiogram.types import CallbackQuery, Message
from keyboards.main_menu import main_menu_kb
from database import AsyncSessionLocal
from models.user import User
from utils.logger import logger

router = Router()

@router.callback_query(lambda c: c.data == "profile")
async def show_profile(cb: CallbackQuery):
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(User).where(User.telegram_id == cb.from_user.id))
        user = q.scalar_one_or_none()
        if not user:
            await cb.message.answer("Профиль не найден. /start")
            return
        text = f"ID: {user.telegram_id}\nИмя: {user.name}\nЯзык: {user.language}\nГород: {user.city or '-'}"
        await cb.message.answer(text, reply_markup=main_menu_kb(user.language))
