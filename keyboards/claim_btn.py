from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


claim = types.ReplyKeyboardMarkup(resize_keyboard=True)
prohibited_content = types.KeyboardButton("18+ 🔞")
advertisement = types.KeyboardButton("Реклама 💵")
spam = types.KeyboardButton("Спам")
back = types.KeyboardButton("Назад")

claim.add(prohibited_content, advertisement, spam, back)

markup = InlineKeyboardMarkup(row_width=1)
add_photo = InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo')
next = InlineKeyboardButton(text='Далее', callback_data='next')
quit = InlineKeyboardButton(text='Отменить', callback_data='quit')

markup.add(add_photo, next, quit)
