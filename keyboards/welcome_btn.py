from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

walcome_markup = InlineKeyboardMarkup(row_width=2)
walcome_markup.add(InlineKeyboardButton(text="👨Парень", callback_data="man"),
                  InlineKeyboardButton(text="👩Девушка", callback_data="woman"))