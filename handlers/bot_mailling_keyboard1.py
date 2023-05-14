from aiogram import types, Dispatcher
from create_bot import dp, bot, db
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from states import FCMAilingK1
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import admins
# from aiogram.dispatcher.filters import Text

# @dp.message_handler(ISPrivate(), text='/maillingk1', chat_id=admins)
async def start_mailling(message: types.Message):
	await message.answer(f'Введите текст рассылки:')
	await FCMAilingK1.text.set()

# @dp.message_handler(ISPrivate(), state=FCMAilingK1.text, chat_id=admins)
async def mailling_text(message: types.Message, state: FSMContext):
	answer = message.text
	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Добавить кнопку', callback_data='button'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await state.update_data(text=answer)
	await message.answer(text=answer, reply_markup=markup)
	await FCMAilingK1.state.set()




# @dp.calback_query_handler(text='button', state=FCMAilingK1.state)
async def add_button(call: types.CallbackQuery):
	await call.message.answer('Пришлите название кнопки и через ":" ссылку')
	await FCMAilingK1.button_name.set()


# @dp.calback_query_handler(state=FCMAilingK1.button_name)
async def button(message: types.Message, state: FSMContext):
	answer = (message.text).split(": ")
	data = await state.get_data()
	text = data.get('text')
	# markup = InlineKeyboardMarkup(row_width=2,
	# 								inline_keyboard=[
	# 									[
	# 										InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
	# 										InlineKeyboardButton(text='Добавить ссылку', callback_data='url'),
	# 										InlineKeyboardButton(text='Отменить', callback_data='quit')
	# 									]
	# 								])
	markup = InlineKeyboardMarkup(row_width=1,
								inline_keyboard=[
									[
										InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
										InlineKeyboardButton(text='Далее', callback_data='nex'),
										InlineKeyboardButton(text='Отменить', callback_data='quit')
									]
								])
	await state.update_data(button_name=answer[0], button_url=answer[1])
	await message.answer(text=answer, reply_markup=markup)
	await FCMAilingK1.state.set()

# # @dp.calback_query_handler(text='url', state=FCMAilingK1.state)
# async def add_url(call: types.CallbackQuery):
# 	await call.message.answer('Пришлите ссылку кнопки')
# 	await FCMAilingK1.button_url.set()


# # @dp.calback_query_handler(state=FCMAilingK1.button_url)
# async def url(message: types.Message, state: FSMContext):
# 	answer = message.text
# 	data = await state.get_data()
# 	text = data.get('text')
# 	button_name = data.get('button_name')
# 	markup = InlineKeyboardMarkup(row_width=2,
# 									inline_keyboard=[
# 										[
# 											InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
# 											InlineKeyboardButton(text='Далее', callback_data='nex'),
# 											InlineKeyboardButton(text='Отменить', callback_data='quit')
# 										]
# 									])
# 	await state.update_data(button_url=answer)

# 	await message.answer(text='123', reply_markup=markup)
# 	await FCMAilingK1.state.set()

# @dp.calback_query_handler(text='nex', state=FCMAilingK1.state)
async def nex(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	text = data.get('text')
	button_name = data.get('button_name')
	button_url = data.get('button_url')

	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
											InlineKeyboardButton(text='Далее', callback_data='next'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])

	mark = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text=button_name, url=f'{button_url}')
										]
									])
	await dp.bot.send_message(call.from_user.id, text=text, reply_markup=mark)

	await dp.bot.send_message(call.from_user.id, text='Готовность', reply_markup=markup)
	await FCMAilingK1.state.set()




# @dp.calback_query_handler(text='next', state=FCMAilingK1.state)
async def start(call: types.CallbackQuery, state: FSMContext):
	users = db.get_users()
	data = await state.get_data()
	text = data.get('text')
	button_name = data.get('button_name')
	button_url= data.get('button_url')
	await state.finish()

	mark = InlineKeyboardMarkup(row_width=2,
								inline_keyboard=[
									[
										InlineKeyboardButton(text=button_name, url=f'{button_url}')
									]
								])

	for user in users:
		try:
			await dp.bot.send_message(chat_id=user[0], text=text, reply_markup=mark)
			await sleep(0.33)
		except Exception:
			pass
	await call.message.answer('Рассылка выполнена')


# @dp.calback_query_handler(text='add_photo', state=FCMAilingK1.state)
async def add_photo(call: types.CallbackQuery):
	await call.message.answer('Пришлите фото')
	await FCMAilingK1.photo.set()

# @dp.message_handler(ISPrivate(), state=FCMAilingK1.photo, content_types=types.ContentType.PHOTO)
async def mailling_photo(message: types.Message, state: FSMContext):
	photo_file_id = message.photo[-1].file_id
	await state.update_data(photo=photo_file_id)
	data = await state.get_data()
	text = data.get('text')
	photo = data.get('photo')
	button_name = data.get('button_name')
	button_url = data.get('button_url')
	mark = InlineKeyboardMarkup(row_width=1,
										inline_keyboard=[
											[
												InlineKeyboardButton(text=button_name, url=f'{button_url}')
											]
										])
	await message.answer(text=text, reply_markup=mark)
	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Далее', callback_data='next'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await message.answer_photo(photo=photo, caption=text, reply_markup=mark)
	await message.answer(text='Готовность', reply_markup=markup)

# @dp.calback_query_handler(text='next', state=FCMAilingK1.photo)
async def start_p(call: types.CallbackQuery, state: FSMContext):
	users = db.get_users()
	data = await state.get_data()
	text = data.get('text')
	photo = data.get('photo')
	button_name = data.get('button_name')
	button_url = data.get('button_url')
	await state.finish()

	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Далее', callback_data='next'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])

	mark = InlineKeyboardMarkup(row_width=1,
										inline_keyboard=[
											[
												InlineKeyboardButton(text=button_name, url=f'{button_url}')
											]
										])
	for user in users:
		try:
			await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text, reply_markup=mark)
			await sleep(0.33)
		except Exception:
			pass
	await call.message.answer('Рассылка выполнена')

# @dp.message_handler(ISPrivate(), state=FCMAilingK1.photo)
async def no_photo(message: types.Message):
	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await message.answer('Пришлите фото', reply_markup=markup)

# @dp.calback_query_handler(text='quit', state=[FCMAilingK1.text, FCMAilingK1.photo, FCMAilingK1.state])
async def quit(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await call.message.answer('Рассылка отменена')


#Регистрируем хендлеры
def register_handlers_bot_mailling_keyboard1(dp: Dispatcher):
	dp.register_callback_query_handler(add_button, text='button', state=FCMAilingK1.state, chat_id=admins)
	dp.register_message_handler(button, state=FCMAilingK1.button_name, chat_id=admins)
	# dp.register_callback_query_handler(add_url, text='url', state=FCMAilingK1.state, chat_id=admins)
	# dp.register_message_handler(url, state=FCMAilingK1.button_url, chat_id=admins)

	dp.register_callback_query_handler(nex, text='nex', state=FCMAilingK1.state, chat_id=admins)



	dp.register_message_handler(start_mailling, text='/maillingk1', chat_id=admins)
	dp.register_message_handler(mailling_text, state=FCMAilingK1.text, chat_id=admins)
	dp.register_callback_query_handler(start, text='next', state=FCMAilingK1.state, chat_id=admins)
	dp.register_callback_query_handler(add_photo, text='add_photo', state=FCMAilingK1.state, chat_id=admins)
	dp.register_message_handler(mailling_photo,state=FCMAilingK1.photo, content_types=types.ContentType.PHOTO, chat_id=admins)
	dp.register_callback_query_handler(start_p, text='next', state=FCMAilingK1.photo, chat_id=admins)
	dp.register_message_handler(no_photo, state=FCMAilingK1.photo, chat_id=admins)
	dp.register_callback_query_handler(quit, text='quit', state=[FCMAilingK1.text, FCMAilingK1.photo, FCMAilingK1.state], chat_id=admins)
