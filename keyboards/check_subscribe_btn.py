from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS


def showChannels():
	channels_keyboard = InlineKeyboardMarkup(row_width=1)

	for channel in CHANNELS:
		channels_btn = InlineKeyboardButton(text=channel[0], url=channel[2])
		channels_keyboard.insert(channels_btn)

	btnDoneSub = InlineKeyboardButton(text='Я подписался ✅', callback_data = 'subchanneldone')
	channels_keyboard.insert(btnDoneSub)
	return channels_keyboard