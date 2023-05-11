from aiogram.dispatcher.filters.state import State, StatesGroup

class FCMBlock(StatesGroup):
	id = State()
	state = State()
