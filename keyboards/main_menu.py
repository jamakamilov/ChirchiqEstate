from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import settings

def language_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🇺🇿 Uzbek"), KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇬🇧 English"))
    return kb

def main_menu_kb(lang="uz"):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔍 Поиск", callback_data="search"))
    kb.add(InlineKeyboardButton("➕ Создать объявление", callback_data="create_listing"))
    kb.add(InlineKeyboardButton("❤ Избранное", callback_data="favorites"))
    kb.add(InlineKeyboardButton("👤 Профиль", callback_data="profile"))
    return kb
