from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

rating_markup = InlineKeyboardMarkup(row_width=2)
rating_markup.add(InlineKeyboardButton(text="👍", callback_data="like"),
                  InlineKeyboardButton(text="👎", callback_data="dislike"))