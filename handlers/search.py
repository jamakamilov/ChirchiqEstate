from aiogram import Router
from aiogram.types import CallbackQuery, Message
from database import AsyncSessionLocal
from models.listing import Listing
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.maps import osm_link
from services.analytics import record_view

router = Router()

@router.callback_query(lambda c: c.data == "search")
async def start_search(cb: CallbackQuery):
    await cb.message.answer("Введите фильтр: район, min-max цена, комнаты (пример: Mirzo, 10000000-50000000, 2)")
    await cb.answer()

@router.message()
async def search_text(message: Message):
    text = message.text
    parts = [p.strip() for p in text.split(",")]
    region = parts[0] if parts else None
    price_min = price_max = None
    rooms = None
    if len(parts) > 1 and "-" in parts[1]:
        pparts = parts[1].split("-")
        try:
            price_min = float(pparts[0])
            price_max = float(pparts[1])
        except:
            pass
    if len(parts) > 2:
        try:
            rooms = int(parts[2])
        except:
            pass
    async with AsyncSessionLocal() as session:
        q = __import__("sqlalchemy").select(Listing).where(Listing.status == "published")
        if region:
            q = q.where(Listing.region.ilike(f"%{region}%"))
        if price_min is not None:
            q = q.where(Listing.price >= price_min)
        if price_max is not None:
            q = q.where(Listing.price <= price_max)
        if rooms is not None:
            q = q.where(Listing.rooms == rooms)
        res = await session.execute(q.limit(20))
        listings = res.scalars().all()
        if not listings:
            await message.answer("Ничего не найдено")
            return
        for l in listings:
            text = f"{l.category} | {l.deal_type}\n{l.region} {l.district or ''}\nЦена: {int(l.price) if l.price else '-'}\nКомнат: {l.rooms}\n{l.description[:200]}"
            kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Написать продавцу", callback_data=f"contact_{l.id}"))
            if l.photos:
                await message.answer_photo(l.photos[0], caption=text, reply_markup=kb)
            else:
                await message.answer(text, reply_markup=kb)
            await record_view(l.id, message.from_user.id)
