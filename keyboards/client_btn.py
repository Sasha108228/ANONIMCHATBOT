from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


find_partner = types.ReplyKeyboardMarkup(resize_keyboard=True)
find_partner_btn = types.KeyboardButton("Искаль партёра 🔍")
menu_btn = types.KeyboardButton("Главная 📝")
find_partner.add(find_partner_btn, menu_btn)

stop_searching = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop_searching_btn = types.KeyboardButton("Остановить поиск ❌")
stop_searching.add(stop_searching_btn)

disconnected = types.ReplyKeyboardMarkup(resize_keyboard=True)
disconnected_btn = types.KeyboardButton("Отключиться 🚫")
menu_btn = types.KeyboardButton("Главная 📝")
claim = types.KeyboardButton("Жалоба ⚠️")
disconnected.add(disconnected_btn, menu_btn, claim)