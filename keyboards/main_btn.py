from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


main = InlineKeyboardMarkup(row_width=2)
profile_btn = InlineKeyboardButton(text='Топ пользователей', callback_data = 'top_num_chats')
questionnaire_btn = InlineKeyboardButton(text='Моя анкета', callback_data='questionnaire')
main.add(profile_btn, questionnaire_btn)

#----------------------------------------------------------------------------------------------------------------

questionnaire = InlineKeyboardMarkup(row_width=2)
edit_questionnaire = InlineKeyboardButton(text='Изменить анкету', callback_data='edit_questionnaire')
questionnaire.add(edit_questionnaire)