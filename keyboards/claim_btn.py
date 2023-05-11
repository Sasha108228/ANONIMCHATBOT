from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


claim = types.ReplyKeyboardMarkup(resize_keyboard=True)
prohibited_content = types.KeyboardButton("18+ 🔞")
advertisement = types.KeyboardButton("Реклама 💵")
spam = types.KeyboardButton("Спам")
back = types.KeyboardButton("Назад")

claim.add(prohibited_content, advertisement, spam, back)
