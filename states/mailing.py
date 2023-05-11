from aiogram.dispatcher.filters.state import State, StatesGroup

class FCMAiling(StatesGroup):
	text = State()
	state = State()
	photo = State()