from aiogram.dispatcher.filters.state import State, StatesGroup

class FCMAilingK1(StatesGroup):
	text = State()
	state = State()
	button_name = State()
	button_url = State()
	photo = State()