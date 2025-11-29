from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from utils.validators import validate_price

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("deal_"))
async def deal_chosen(cb: CallbackQuery, state: FSMContext):
    deal = cb.data.split("_",1)[1]
    await state.update_data(deal_type=deal)
    await cb.message.answer("Укажите регион и район (через запятую)")
    await state.set_state("listing_region")

@router.message()
async def region_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_region":
        return
    text = message.text
    parts = [p.strip() for p in text.split(",")]
    region = parts[0] if parts else None
    district = parts[1] if len(parts) > 1 else None
    await state.update_data(region=region, district=district)
    await message.answer("Укажите цену (только цифры)")
    await state.set_state("listing_price")

@router.message()
async def price_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_price":
        return
    price = validate_price(message.text)
    if price is None:
        await message.answer("Неверная цена. Попробуйте ещё раз.")
        return
    await state.update_data(price=price)
    await message.answer("Укажите площадь (м²)")
    await state.set_state("listing_area")
