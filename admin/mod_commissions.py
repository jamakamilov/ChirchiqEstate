from aiogram import Router
from aiogram.types import CallbackQuery, Message
from database import AsyncSessionLocal
from models.commissions import Commission
from config import settings

router = Router()

@router.callback_query(lambda c: c.data == "admin_commissions")
async def show_commissions(cb: CallbackQuery):
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(Commission))
        cs = q.scalars().all()
        text = "Комиссии:\n"
        for c in cs:
            text += f"{c.id}: {c.percent}%\n"
        await cb.message.answer(text)
