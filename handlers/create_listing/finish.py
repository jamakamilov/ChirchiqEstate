from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import AsyncSessionLocal
from models.listing import Listing
from models.user import User
from utils.logger import logger

router = Router()

@router.message(commands=["done"])
async def finish_listing(message: Message, state: FSMContext):
    data = await state.get_data()
    # minimal validation
    required = ["category", "deal_type", "region", "price", "area", "floor", "rooms", "description", "coords"]
    for r in required:
        if r not in data:
            await message.answer("Не все поля заполнены. Начните заново /create_listing")
            return
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(User).where(User.telegram_id == message.from_user.id))
        user = q.scalar_one_or_none()
        if not user:
            await message.answer("Пользователь не найден")
            return
        listing = Listing(
            owner_id=user.id,
            category=data["category"],
            deal_type=data["deal_type"],
            region=data.get("region"),
            district=data.get("district"),
            price=data.get("price"),
            area=data.get("area"),
            floor=data.get("floor"),
            floors_total=data.get("floors_total"),
            rooms=data.get("rooms"),
            description=data.get("description"),
            coords=data.get("coords"),
            photos=data.get("photos", []),
            status="moderation"
        )
        session.add(listing)
        await session.commit()
        await session.refresh(listing)
        await message.answer("Объявление отправлено на модерацию")
        logger.info(f"Listing {listing.id} created by user {user.telegram_id}")
        await state.clear()
