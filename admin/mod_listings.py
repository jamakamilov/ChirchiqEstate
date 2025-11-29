from aiogram import Router
from aiogram.types import CallbackQuery
from database import AsyncSessionLocal
from models.listing import Listing
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import settings
from services.notifications import bot

router = Router()

@router.callback_query(lambda c: c.data == "admin_mod_listings")
async def mod_listings(cb: CallbackQuery):
    # list listings in moderation
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(Listing).where(Listing.status == "moderation"))
        listings = q.scalars().all()
        if not listings:
            await cb.message.answer("Нет объявлений на модерации")
            return
        for l in listings:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Одобрить", callback_data=f"approve_{l.id}"))
            kb.add(InlineKeyboardButton("Отклонить", callback_data=f"reject_{l.id}"))
            if l.photos:
                await cb.message.answer_photo(l.photos[0], caption=f"{l.id} | {l.region} | {l.price}", reply_markup=kb)
            else:
                await cb.message.answer(f"{l.id} | {l.region} | {l.price}", reply_markup=kb)

@router.callback_query(lambda c: c.data and c.data.startswith("approve_"))
async def approve(cb: CallbackQuery):
    lid = int(cb.data.split("_",1)[1])
    async with AsyncSessionLocal() as session:
        q = await session.execute(__import__("sqlalchemy").select(Listing).where(Listing.id == lid))
        l = q.scalar_one_or_none()
        if not l:
            await cb.message.answer("Не найдено")
            return
        l.status = "published"
        from sqlalchemy import func
        l.published_at = func.now()
        await session.commit()
        # publish to channel
        channel = settings.CHANNEL_ID
        caption = f"{l.category} | {l.deal_type}\n{l.region} {l.district or ''}\nЦена: {int(l.price) if l.price else '-'}\nКомнат: {l.rooms}\n{l.description[:300]}"
        if l.photos:
            try:
                await bot.send_photo(channel, l.photos[0], caption=caption)
            except Exception as e:
                await cb.message.answer(f"Ошибка публикации: {e}")
        await cb.message.answer("Объявление одобрено и опубликовано")
