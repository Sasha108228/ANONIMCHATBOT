from aiogram import types, Dispatcher
from create_bot import dp, bot, db
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from states import FCMAiling
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import admins

# from aiogram.dispatcher.filters import Text

# @dp.message_handler(ISPrivate(), text='/mailling', chat_id=admins)
async def start_mailling(message: types.Message):
	await message.answer(f'Введите текст рассылки:')
	await FCMAiling.text.set()

# @dp.message_handler(ISPrivate(), state=FCMAiling.text, chat_id=admins)
async def mailling_text(message: types.Message, state: FSMContext):
	answer = message.text
	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
											InlineKeyboardButton(text='Далее', callback_data='next'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await state.update_data(text=answer)
	await message.answer(text=answer, reply_markup=markup)
	await FCMAiling.state.set()


# @dp.calback_query_handler(text='next', state=FCMAiling.state)
async def start(call: types.CallbackQuery, state: FSMContext):
	users = db.get_users()
	data = await state.get_data()
	text = data.get('text')
	await state.finish()
	for user in users:
		try:
			await dp.bot.send_message(chat_id=user[0], text=text)
			await sleep(0.33)
		except Exception:
			pass
	await call.message.answer('Рассылка выполнена')


# @dp.calback_query_handler(text='add_photo', state=FCMAiling.state)
async def add_photo(call: types.CallbackQuery):
	await call.message.answer('Пришлите фото')
	await FCMAiling.photo.set()

# @dp.message_handler(ISPrivate(), state=FCMAiling.photo, content_types=types.ContentType.PHOTO)
async def mailling_photo(message: types.Message, state: FSMContext):
	photo_file_id = message.photo[-1].file_id
	await state.update_data(photo=photo_file_id)
	data = await state.get_data()
	text = data.get('text')
	photo = data.get('photo')
	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Далее', callback_data='next'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await message.answer_photo(photo=photo, caption=text, reply_markup=markup)

# @dp.calback_query_handler(text='next', state=FCMAiling.photo)
async def start_p(call: types.CallbackQuery, state: FSMContext):
	users = db.get_users()
	data = await state.get_data()
	text = data.get('text')
	photo = data.get('photo')
	await state.finish()
	for user in users:
		try:
			await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
			await sleep(0.33)
		except Exception:
			pass
	await call.message.answer('Рассылка выполнена')

# @dp.message_handler(ISPrivate(), state=FCMAiling.photo)
async def no_photo(message: types.Message):
	markup = InlineKeyboardMarkup(row_width=1,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await message.answer('Пришлите фото', reply_markup=markup)

# @dp.calback_query_handler(text='quit', state=[FCMAiling.text, FCMAiling.photo, FCMAiling.state])
async def quit(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await call.message.answer('Рассылка отменена')


#Регистрируем хендлеры
def register_handlers_bot_mailling(dp: Dispatcher):
	dp.register_message_handler(start_mailling, text='/mailling', chat_id=admins)
	dp.register_message_handler(mailling_text, state=FCMAiling.text, chat_id=admins)
	dp.register_callback_query_handler(start, text='next', state=FCMAiling.state, chat_id=admins)
	dp.register_callback_query_handler(add_photo, text='add_photo', state=FCMAiling.state, chat_id=admins)
	dp.register_message_handler(mailling_photo,state=FCMAiling.photo, content_types=types.ContentType.PHOTO, chat_id=admins)
	dp.register_callback_query_handler(start_p, text='next', state=FCMAiling.photo, chat_id=admins)
	dp.register_message_handler(no_photo, state=FCMAiling.photo, chat_id=admins)
	dp.register_callback_query_handler(quit, text='quit', state=[FCMAiling.text, FCMAiling.photo, FCMAiling.state], chat_id=admins)
