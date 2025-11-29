from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()

@router.message()
async def area_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_area":
        return
    try:
        area = float(message.text.replace(",", "."))
    except:
        await message.answer("Неверная площадь")
        return
    await state.update_data(area=area)
    await message.answer("Этаж / Всего этажей (пример: 3/9)")
    await state.set_state("listing_floor")

@router.message()
async def floor_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_floor":
        return
    parts = message.text.split("/")
    try:
        floor = int(parts[0])
        floors_total = int(parts[1]) if len(parts) > 1 else None
    except:
        await message.answer("Неверный формат. Пример: 3/9")
        return
    await state.update_data(floor=floor, floors_total=floors_total)
    await message.answer("Количество комнат (число)")
    await state.set_state("listing_rooms")

@router.message()
async def rooms_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_rooms":
        return
    try:
        rooms = int(message.text)
    except:
        await message.answer("Неверное число комнат")
        return
    await state.update_data(rooms=rooms)
    await message.answer("Краткое описание")
    await state.set_state("listing_description")
