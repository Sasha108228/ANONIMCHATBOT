from create_bot import dp, bot, db, check_sub_channels
from keyboards import check_subscribe_btn as nav
import config as con
from aiogram import types, Dispatcher
from keyboards import client_btn as navs


from states import FSMWelcome
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

#----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
# 	if message.chat.type == 'private':
# 		if await check_sub_channels(con.CHANNELS, message.from_user.id):
# 			await bot.send_message(message.from_user.id, 'Hi', reply_markup = nav.profileKeyboard)
# 		else:
# 			await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())

#----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler()
# async def bot_message(message: types.Message):
# 	if message.chat.type == 'private':
# 		if await check_sub_channels(con.CHANNELS, message.from_user.id):
# 			if message.text == 'Profile':
# 				await bot.send_message(message.from_user.id, f'ID: {message.from_user.id}')
# 		else:
# 			await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='subchanneldone')
async def subchanneldone(callback_query: types.CallbackQuery):
	await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
	await bot.answer_callback_query(callback_query.id)

	if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):
		await callback_query.answer(" Привет, я Анонимный ЧатБот!")
		await bot.send_message(callback_query.from_user.id, 'Напишите /start')
	else:
		await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())
		await bot.answer_callback_query(callback_query.id)



# #----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.name)
# async def load_name(message: types.Message, state: FSMContext):
# 	async with state.proxy() as data:
# 		data['name'] = message.text
# 		db.set_name(message.from_user.id, message.text)
# 		await message.answer('Введите возраст')
# 		await FSMWelcome.next()

# #----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.age)
# async def load_age(message: types.Message, state: FSMContext):
# 	async with state.proxy() as data:
# 		data['age'] = message.text
# 		db.set_age(message.from_user.id, message.text)
# 		await message.answer('Введите описание, которое будут видеть люди с которыми вы будете общаться')
# 		await FSMWelcome.next()

# #----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.text)
# async def load_text(message: types.Message, state: FSMContext):
# 	async with state.proxy() as data:
# 		data['text'] = message.text
# 		db.set_text(message.from_user.id, message.text)
# 		await message.answer('Анкета заполнена, удачного общения!', reply_markup=navs.find_partner)
# 		await state.finish()

# #----------------------------------------------------------------------------------------------------------------




#Регистрируем хендлеры
def register_handlers_check_subscribe(dp: Dispatcher):
	# dp.register_message_handler(start, commands=['start'])
	# dp.register_message_handler(bot_message)
	dp.register_callback_query_handler(subchanneldone, text='subchanneldone')
	# dp.register_message_handler(load_name, state=FSMWelcome.name)
	# dp.register_message_handler(load_age, state=FSMWelcome.age)
	# dp.register_message_handler(load_text, state=FSMWelcome.text)