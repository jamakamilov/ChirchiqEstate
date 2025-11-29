from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def payment_actions():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Отправить скрин", callback_data="send_screenshot"))
    kb.add(InlineKeyboardButton("Отмена", callback_data="cancel_payment"))
    return kb
