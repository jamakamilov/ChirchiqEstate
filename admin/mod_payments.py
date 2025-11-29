from aiogram import Router
from aiogram.types import CallbackQuery
from services.payments import list_pending, set_payment_status

router = Router()

@router.callback_query(lambda c: c.data == "admin_mod_payments")
async def mod_payments(cb: CallbackQuery):
    pending = await list_pending()
    if not pending:
        await cb.message.answer("Нет ожидающих оплат")
        return
    for p in pending:
        kb = __import__("aiogram.types").InlineKeyboardMarkup()
        kb.add(__import__("aiogram.types").InlineKeyboardButton("Подтвердить", callback_data=f"pay_approve_{p.id}"))
        kb.add(__import__("aiogram.types").InlineKeyboardButton("Отклонить", callback_data=f"pay_reject_{p.id}"))
        await cb.message.answer(f"Оплата {p.id} от {p.user_id} сумма {p.amount}", reply_markup=kb)

@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def handle_pay(cb: CallbackQuery):
    parts = cb.data.split("_")
    action = parts[1]
    pid = int(parts[2])
    if action == "approve":
        await set_payment_status(pid, "approved")
        await cb.message.answer("Оплата подтверждена")
    else:
        await set_payment_status(pid, "rejected")
        await cb.message.answer("Оплата отклонена")
