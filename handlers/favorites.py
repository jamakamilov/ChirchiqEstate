from aiogram import Router
from aiogram.types import CallbackQuery
from database import AsyncSessionLocal
from models.favorites import Favorite
from models.user import User
from models.listing import Listing

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("fav_"))
async def fav_action(cb: CallbackQuery):
    parts = cb.data.split("_")
    action = parts[1]
    listing_id = int(parts[2])
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(User).where(User.telegram_id == cb.from_user.id))
        user = q.scalar_one_or_none()
        if not user:
            await cb.message.answer("Пользователь не найден")
            return
        if action == "add":
            fav = Favorite(user_id=user.id, listing_id=listing_id)
            session.add(fav)
            await session.commit()
            await cb.message.answer("Добавлено в избранное")
        elif action == "remove":
            q2 = await session.execute(__import__("sqlalchemy").select(Favorite).where(Favorite.user_id == user.id, Favorite.listing_id == listing_id))
            f = q2.scalar_one_or_none()
            if f:
                await session.delete(f)
                await session.commit()
                await cb.message.answer("Удалено из избранного")
