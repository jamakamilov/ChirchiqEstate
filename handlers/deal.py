from aiogram import Router
from aiogram.types import Message, CallbackQuery
from database import AsyncSessionLocal
from models.commissions import CommissionRequest, Commission
from models.user import User
from utils.formatter import format_price
from config import settings

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("deal_"))
async def deal_flow(cb: CallbackQuery):
    # placeholder for deal completion flow
    await cb.message.answer("Чтобы завершить сделку, отправьте сумму продажи (число)")
    await cb.message.answer("Пример: 150000000")
    await cb.answer()
    # In production, set FSM state and continue
