from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def category_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Квартира", callback_data="cat_apartment"))
    kb.add(InlineKeyboardButton("Дом", callback_data="cat_house"))
    kb.add(InlineKeyboardButton("Земля", callback_data="cat_land"))
    return kb

def deal_type_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Продажа", callback_data="deal_sale"))
    kb.add(InlineKeyboardButton("Аренда", callback_data="deal_rent"))
    return kb
