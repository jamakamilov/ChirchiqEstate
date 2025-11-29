from aiogram import Router
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext

router = Router()

@router.message()
async def description_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_description":
        return
    await state.update_data(description=message.text)
    await message.answer("Отправьте координаты в формате: lat,lon или отправьте геолокацию")
    await state.set_state("listing_coords")

@router.message(content_types=[ContentType.LOCATION])
async def location_received(message: Message, state: FSMContext):
    loc = {"lat": message.location.latitude, "lon": message.location.longitude}
    await state.update_data(coords=loc)
    await message.answer("Теперь отправьте 1-10 фото объекта. Когда закончите — напишите /done")
    await state.set_state("listing_photos")

@router.message()
async def coords_text(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_coords":
        return
    parts = [p.strip() for p in message.text.split(",")]
    if len(parts) != 2:
        await message.answer("Неверный формат. Пример: 41.3,69.2")
        return
    try:
        lat = float(parts[0])
        lon = float(parts[1])
    except:
        await message.answer("Неверные координаты")
        return
    await state.update_data(coords={"lat": lat, "lon": lon})
    await message.answer("Теперь отправьте 1-10 фото объекта. Когда закончите — напишите /done")
    await state.set_state("listing_photos")

@router.message(content_types=[ContentType.PHOTO])
async def photo_received(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name != "listing_photos":
        return
    data = await state.get_data()
    photos = data.get("photos", [])
    file_id = message.photo[-1].file_id
    photos.append(file_id)
    await state.update_data(photos=photos)
    await message.answer(f"Фото принято ({len(photos)})")
