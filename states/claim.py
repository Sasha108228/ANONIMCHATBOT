from aiogram.dispatcher.filters.state import State, StatesGroup

class FCMClaim(StatesGroup):
	text = State()
	state = State()
	photo = State()

