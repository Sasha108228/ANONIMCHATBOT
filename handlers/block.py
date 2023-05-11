from create_bot import dp, bot, db, check_sub_channels
from config import admins
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import FCMBlock
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# @dp.message_handler(text='/block', chat_id=admins)
async def start_block(message: types.Message):
	await message.answer(f'Введите текст id пользователя, которого нужно заблокировать:')
	await FCMBlock.id.set()

# @dp.message_handler(state=FCMBlock.id, chat_id=admins)
async def block_check(message: types.Message, state: FSMContext):
	answer = message.text
	markup = InlineKeyboardMarkup(row_width=2,
									inline_keyboard=[
										[
											InlineKeyboardButton(text='Далее', callback_data='next'),
											InlineKeyboardButton(text='Отменить', callback_data='quit')
										]
									])
	await state.update_data(id=answer)
	await message.answer(text=answer, reply_markup=markup)
	await FCMBlock.state.set()


# @dp.calback_query_handler(text='next', state=FCMBlock.state, chat_id=admins)
async def block(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	id = data.get('id')
	await state.finish()

	db.set_block(id)

	await call.message.answer('Пользователь заблокирован!')

# @dp.calback_query_handler(text='quit', state=[FCMBlock.id, FCMBlock.state], chat_id=admins)
async def quit(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await call.message.answer('Блокировка отменена!')


#Регистрируем хендлеры
def register_handlers_block(dp: Dispatcher):
	dp.register_message_handler(start_block, text='/block', chat_id=admins)
	dp.register_message_handler(block_check, state=FCMBlock.id, chat_id=admins)
	dp.register_callback_query_handler(block, text='next', state=FCMBlock.state, chat_id=admins)
	dp.register_callback_query_handler(quit, text='quit', state=[FCMBlock.id, FCMBlock.state], chat_id=admins)