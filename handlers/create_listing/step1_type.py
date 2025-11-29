from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.create_listing_kb import category_kb, deal_type_kb
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(lambda c: c.data == "create_listing")
async def start_create(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("Выберите категорию", reply_markup=category_kb())
    await state.set_state("listing_category")
