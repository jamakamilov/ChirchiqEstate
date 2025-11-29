from aiogram import Router
from aiogram.types import CallbackQuery
from database import AsyncSessionLocal
from models.listing import Listing
from services.recommendation_engine import similar_listings, avg_price_by_region

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("recommend_"))
async def recommend(cb: CallbackQuery):
    listing_id = int(cb.data.split("_",1)[1])
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(Listing).where(Listing.id == listing_id))
        l = q.scalar_one_or_none()
        if not l:
            await cb.message.answer("Объект не найден")
            return
        sims = await similar_listings(l)
        avg = await avg_price_by_region(l.region)
        text = f"Похожие объекты (средняя цена в районе: {int(avg) if avg else '-'}):"
        for s in sims:
            text += f"\n• {s.id} {s.price} {s.rooms}км"
        await cb.message.answer(text)
