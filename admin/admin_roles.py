from aiogram import Router
from aiogram.types import CallbackQuery
from database import AsyncSessionLocal
from models.roles import Role

router = Router()

@router.callback_query(lambda c: c.data == "admin_roles")
async def roles(cb: CallbackQuery):
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(Role))
        roles = q.scalars().all()
        text = "Роли:\n"
        for r in roles:
            text += f"{r.id}: {r.name} paid={r.is_paid}\n"
        await cb.message.answer(text)
