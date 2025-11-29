from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from utils.validators import validate_coords

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("cat_"))
async def category_chosen(cb: CallbackQuery, state: FSMContext):
    cat = cb.data.split("_",1)[1]
    await state.update_data(category=cat)
    await cb.message.answer("Выберите тип сделки", reply_markup=deal_type_kb())
    await state.set_state("listing_deal_type")

from keyboards.create_listing_kb import deal_type_kb
