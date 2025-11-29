from aiogram import Router
from aiogram.types import CallbackQuery, Message
from database import AsyncSessionLocal
from models.roles import Role
from models.user import User
from keyboards.payment_kb import payment_actions
from utils.logger import logger

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("role_"))
async def choose_role(cb: CallbackQuery):
    role_key = cb.data.split("_", 1)[1]
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(Role).where(Role.name == role_key))
        role = q.scalar_one_or_none()
        if not role:
            await cb.message.answer("Role not found")
            return
        if role.is_paid:
            # send payment instructions (manual)
            text = f"Роль {role.name} платная. Отправьте перевод на карту: 8600 0000 0000 0000\nПосле перевода пришлите скрин."
            await cb.message.answer(text, reply_markup=payment_actions())
        else:
            # assign role
            q2 = await session.execute(__import__("sqlalchemy").select(User).where(User.telegram_id == cb.from_user.id))
            user = q2.scalar_one_or_none()
            if user:
                user.role_id = role.id
                await session.commit()
                await cb.message.answer("Роль назначена")
