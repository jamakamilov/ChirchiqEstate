from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Модерация объявлений", callback_data="admin_mod_listings"))
    kb.add(InlineKeyboardButton("Модерация оплат", callback_data="admin_mod_payments"))
    kb.add(InlineKeyboardButton("Комиссии", callback_data="admin_commissions"))
    kb.add(InlineKeyboardButton("Статистика", callback_data="admin_stats"))
    return kb
