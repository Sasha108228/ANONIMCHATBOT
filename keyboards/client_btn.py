from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


# find_partner = types.ReplyKeyboardMarkup(resize_keyboard=True)
# find_partner_btn = types.KeyboardButton("Искать партнёра 🔍")

# profile_btn = types.KeyboardButton("Топ пользователей 📊")
# questionnaire_btn = types.KeyboardButton("Моя анкета 📖")

# # menu_btn = types.KeyboardButton("Главная 📝")
# find_partner.add(find_partner_btn, profile_btn, questionnaire_btn)

find_partner = types.ReplyKeyboardMarkup(
    keyboard=[
        ["Искать партнёра 🔍"],
        ["Топ пользователей 📊", "Моя анкета 📖"]
    ],
    resize_keyboard=True
)



stop_searching = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop_searching_btn = types.KeyboardButton("Остановить поиск ❌")
stop_searching.add(stop_searching_btn)

disconnected = types.ReplyKeyboardMarkup(resize_keyboard=True)
disconnected_btn = types.KeyboardButton("Отключиться 🚫")
claim = types.KeyboardButton("Жалоба ⚠️")
disconnected.add(disconnected_btn, claim)