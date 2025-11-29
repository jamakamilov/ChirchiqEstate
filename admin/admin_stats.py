from aiogram import Router
from aiogram.types import CallbackQuery
from services.analytics import popular_regions

router = Router()

@router.callback_query(lambda c: c.data == "admin_stats")
async def stats(cb: CallbackQuery):
    stats = await popular_regions()
    await cb.message.answer(f"Статистика: {len(stats)} записей")
