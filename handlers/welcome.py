from create_bot import dp, bot, db, check_sub_channels
from db import Database
from aiogram import types, Dispatcher
from states import FSMWelcome
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import welcome_btn as btn
from keyboards import client_btn as nav
from keyboards import check_subscribe_btn as navs
import config as con

# @dp.message_handler(commands = ['start'], state = None)
async def start(message: types.Message):
    if message.chat.type == 'private':
        if(not db.user_exists(message.from_user.id)):
                if await check_sub_channels(con.CHANNELS, message.from_user.id):
                    db.null_block(message.from_user.id)
                    db.add_user(message.from_user.id)
                    db.null_like_dislike(message.from_user.id)
                    await FSMWelcome.name.set()
                    await message.answer(" Привет, я Анонимный ЧатБот!")
                    await bot.send_message(message.from_user.id, 'Заполнение анкетки:')
                    await message.reply('Укажите ваше имя')

                else:
                    await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=navs.showChannels())
        else:
            if(not db.get_block(message.from_user.id)):
                await message.answer(" Привет, я Анонимный ЧатБот!")
                await message.answer(" Пожалуйста нажмите на кнопку для поиска нового собеседника", reply_markup=nav.find_partner)
            else:
                await bot.send_message(message.from_user.id, "Вы заблокированы!")

    else:
        await bot.send_message(message.from_user.id, 'Бот работает только в приватных чатах!')

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FSMWelcome.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        db.set_name(message.from_user.id, message.text)
        await message.answer('Введите возраст')
        await FSMWelcome.next()

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FSMWelcome.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
        db.set_age(message.from_user.id, message.text)
        await message.answer('Введите описание, которое будут видеть люди с которыми вы будете общаться')
        await FSMWelcome.next()

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FSMWelcome.text)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        db.set_text(message.from_user.id, message.text)
        await message.answer('Выберите свой пол', reply_markup=btn.walcome_markup)
        await FSMWelcome.next()

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='man', state=FSMWelcome.gender)
async def load_gender_man(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # data['gender'] = message.text
        data['gender'] = 'Мужчина'
        db.set_gender(callback_query.from_user.id, data['gender'])
        await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!', reply_markup=nav.find_partner)
        await state.finish()

# @dp.callback_query_handler(text='woman', state=FSMWelcome.gender)
async def load_gender_woman(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # data['gender'] = message.text
        data['gender'] = 'Женщина'
        db.set_gender(callback_query.from_user.id, data['gender'])
        await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!', reply_markup=nav.find_partner)
        await state.finish()


#----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.gender)
# async def load_gender(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         # data['gender'] = message.text
#         db.set_gender(message.from_user.id, data['gender'])
#         await message.answer('Анкета заполнена, удачного общения!', reply_markup=nav.find_partner)
#         await state.finish()



# # @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     if message.chat.type == 'private':
#         if await check_sub_channels(con.CHANNELS, message.from_user.id):
#             await message.answer(" Привет, я Анонимный ЧатБот!")
#             await message.answer(" Пожалуйста нажмите на кнопку для поиска нового собеседника", reply_markup=nav.find_partner)
#         else:
#             await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())

#----------------------------------------------------------------------------------------------------------------

#Регистрируем хендлеры
def register_handlers_welcome(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state = None)
    dp.register_message_handler(load_name, state=FSMWelcome.name)
    dp.register_message_handler(load_age, state=FSMWelcome.age)
    dp.register_message_handler(load_text, state=FSMWelcome.text)
    dp.register_callback_query_handler(load_gender_man, text='man', state=FSMWelcome.gender)
    dp.register_callback_query_handler(load_gender_woman, text='woman', state=FSMWelcome.gender)
