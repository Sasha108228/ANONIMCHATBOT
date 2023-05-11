from create_bot import dp, bot, db, check_sub_channels
from keyboards import main_btn as nav
import config as con
from aiogram import types, Dispatcher
from keyboards import client_btn as navs
from keyboards import welcome_btn as btn
from states import FSMWelcome
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(lambda message: message.text == "Главная 📝")
async def main(message: types.Message):
	if db.get_block(message.from_user.id) == 0:

		chat = db.get_chat(message.from_user.id)

		if chat:

			await message.answer("Вы оключились от чата!", reply_markup = navs.find_partner)
			await message.answer("Главная", reply_markup=nav.main)
			await bot.send_message(chat[1], "Парнёр отключился!", reply_markup = navs.find_partner)
			await bot.send_message(chat[1], "Главная", reply_markup=nav.main)
			db.delete_chat(message.from_user.id)

		else:
			await message.answer("Главная", reply_markup=nav.main)
	else:
		await bot.send_message(message.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='top_num_chats')
async def top_num_chats(callback_query: types.CallbackQuery):
	if db.get_block(callback_query.from_user.id) == 0:

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, f"""Топ пользователей:
			{db.get_top_num_chats()}
			""")

	else:
	    await bot.send_message(message.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='questionnaire')
async def questionnaire(callback_query: types.CallbackQuery):
	if db.get_block(callback_query.from_user.id) == 0:

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, f"""Ваша анкета:
			Имя: {db.get_name(callback_query.from_user.id)}
			Возраст: {db.get_age(callback_query.from_user.id)}
			Текст: {db.get_text(callback_query.from_user.id)}
			Пол: {db.get_gender(callback_query.from_user.id)}
			Рейтинг:
			Лайки👍: {db.get_like(callback_query.from_user.id)}
			Дизлайки👎: {db.get_dislike(callback_query.from_user.id)}
			Количество диалогов: {db.get_num_chats(callback_query.from_user.id)}
			""", reply_markup = nav.questionnaire)
	else:
		await bot.send_message(message.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='edit_questionnaire')
async def edit_questionnaire(callback_query: types.CallbackQuery):
	if db.get_block(callback_query.from_user.id) == 0:
		await FSMWelcome.name.set()
		await bot.send_message(callback_query.from_user.id, 'Заполнение анкетки:')
		await bot.send_message(callback_query.from_user.id, 'Укажите ваше имя')
	else:
		await bot.send_message(message.from_user.id, "Вы заблокированы!")
# @dp.message_handler(state=FSMWelcome.name)
async def load_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
		db.set_name(message.from_user.id, message.text)
		await message.answer('Введите возраст')
		await FSMWelcome.next()

# @dp.message_handler(state=FSMWelcome.age)
async def load_age(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['age'] = message.text
		db.set_age(message.from_user.id, message.text)
		await message.answer('Введите описание, которое будут видеть люди с которыми вы будете общаться')
		await FSMWelcome.next()


# @dp.message_handler(state=FSMWelcome.text)
async def load_text(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['text'] = message.text
		db.set_text(message.from_user.id, message.text)
		await message.answer('Выберите свой пол', reply_markup=btn.walcome_markup)
		await FSMWelcome.next()

# @dp.callback_query_handler(text='man', state=FSMWelcome.gender)
async def load_gender_man(callback_query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['gender'] = 'Мужчина'
		db.set_gender(callback_query.from_user.id, data['gender'])
		await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!', reply_markup=nav.find_partner)
		await state.finish()

# @dp.callback_query_handler(text='woman', state=FSMWelcome.gender)
async def load_gender_woman(callback_query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['gender'] = 'Женщина'
		db.set_gender(callback_query.from_user.id, data['gender'])
		await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!', reply_markup=nav.find_partner)
		await state.finish()



#----------------------------------------------------------------------------------------------------------------

#Регистрируем хендлеры
def register_handlers_main(dp: Dispatcher):
	dp.register_message_handler(main, lambda message: message.text == "Главная 📝")
	dp.register_callback_query_handler(top_num_chats, text='top_num_chats')
	dp.register_callback_query_handler(questionnaire, text='questionnaire')
	dp.register_callback_query_handler(edit_questionnaire, text='edit_questionnaire')
	dp.register_message_handler(load_name, state=FSMWelcome.name)
	dp.register_message_handler(load_age, state=FSMWelcome.age)
	dp.register_message_handler(load_text, state=FSMWelcome.text)
	dp.register_callback_query_handler(load_gender_man, text='man', state=FSMWelcome.gender)
	dp.register_callback_query_handler(load_gender_woman, text='woman', state=FSMWelcome.gender)