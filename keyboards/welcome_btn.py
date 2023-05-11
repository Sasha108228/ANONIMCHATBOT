from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

walcome_markup = InlineKeyboardMarkup(row_width=2)
walcome_markup.add(InlineKeyboardButton(text="Мужчина", callback_data="man"),
                  InlineKeyboardButton(text="Женщина", callback_data="woman"))