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
import datetime

# @dp.message_handler(commands = ['start'], state = None)
async def start(message: types.Message):
    if message.chat.type == 'private':
        if(not db.user_exists(message.from_user.id)):
                if await check_sub_channels(con.CHANNELS, message.from_user.id):
                    db.null_block(message.from_user.id)
                    db.add_user(message.from_user.id)
                    db.null_like_dislike(message.from_user.id)
                    db.set_data(message.from_user.id, datetime.datetime.now())
                    await FSMWelcome.name.set()
                    await message.answer(" Привет, я Анонимный ЧатБот!")
                    await bot.send_message(message.from_user.id, 'Заполнение анкетки:')
                    await message.reply('Как я могу обращаться к тебе?🤔')

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
#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='edit_questionnaire')
async def edit_questionnaire(callback_query: types.CallbackQuery):
    if db.get_block(callback_query.from_user.id) == 0:
        await FSMWelcome.name.set()
        await bot.send_message(callback_query.from_user.id, 'Заполнение анкетки:')
        await bot.send_message(callback_query.from_user.id, 'Как я могу обращаться к тебе?🤔')
    else:
        await bot.send_message(message.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FSMWelcome.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        max_length = 50  # Максимальное количество символов
        text = message.text
        if len(text) > max_length:
            await bot.send_photo(message.from_user.id, caption = 'Ваше сообщение было отформатировано, так как превышает разрешённые 50 символов. Вы всегда можете изменить свою анкету!', photo = open('Images/404.png', 'rb'))
            text = text[:max_length]
            data['name'] = text
            # await message.reply("Ваше сообщение было отформатировано, так как превышает максимальное количество символов.")
        else:
            data['name'] = text
        db.set_name(message.from_user.id, text)
        await message.answer('Сколько тебе лет?🔞')
        await FSMWelcome.next()

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FSMWelcome.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        age = int(message.text) if message.text.isdigit() else None
        if age is not None:
            if age < 0 or age > 120:
                await bot.send_photo(message.from_user.id, caption = "Был указан некорректный возраст. Установлен возраст '0'.", photo = open('Images/404.png', 'rb'))
                age = "0"
                data['age'] = age
                # await message.reply("Был указан некорректный возраст. Установлен возраст '0'.")
            elif len(age) > 3:
                await bot.send_photo(message.from_user.id, caption = "Был указан некорректный возраст. Установлен возраст '0'.", photo = open('Images/404.png', 'rb'))
                age = "0"
                data['age'] = age
            else:
                data['age'] = age

        # age = message.text.strip()  # Удаляем возможные пробелы вокруг введенного возраста
        # if not age.isdigit():
        #     formatted_text = "0"
        #     await bot.send_photo(message.from_user.id, caption = 'Был указан некорректный возраст. Установлен возраст '0'.', photo = open('Images/404.png', 'rb'))
        #     data['age'] = formatted_text
        # else:
        #     data['age'] = age

        db.set_age(message.from_user.id, age)
        await message.answer('💬 Расскажи немного о себе, кого ты ищешь, чем увлекаешься и т.д.')
        await FSMWelcome.next()

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FSMWelcome.text)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        max_length = 500  # Максимальное количество символов
        text = message.text
        if len(text) > max_length:
            await bot.send_photo(message.from_user.id, caption = 'Ваше сообщение было отформатировано, так как превышает разрешённые 500 символов. Вы всегда можете изменить свою анкету!', photo = open('Images/404.png', 'rb'))
            text = text[:max_length]
            data['text'] = text
            # await message.reply("Ваше сообщение было отформатировано, так как превышает максимальное количество символов.")
        else:
            data['text'] = text
        db.set_text(message.from_user.id, text)
        await message.answer('🚻 Укажи свой пол:', reply_markup=btn.walcome_markup)
        await FSMWelcome.next()

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='man', state=FSMWelcome.gender)
async def load_gender_man(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # data['gender'] = message.text
        data['gender'] = '👨Парень'
        db.set_gender(callback_query.from_user.id, data['gender'])
        await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!')
        await bot.send_message(callback_query.from_user.id, """📜 Правила чата. Прочти перед использованием:
1. Уважайте других участников✊
2. Сохраняйте анонимность🎭
3. Не публикуйте незаконный контент🔞
4. Избегайте спама и рекламы📢

📝 Помните, что администрация бота имеет право изменять правила по своему усмотрению для обеспечения комфортного опыта для всех участников.""", reply_markup=nav.find_partner)
        await state.finish()

# @dp.callback_query_handler(text='woman', state=FSMWelcome.gender)
async def load_gender_woman(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # data['gender'] = message.text
        data['gender'] = '👩Девушка'
        db.set_gender(callback_query.from_user.id, data['gender'])
        await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!')
        await bot.send_message(callback_query.from_user.id, """📜 Правила чата. Прочти перед использованием:
1. Уважайте других участников✊
2. Сохраняйте анонимность🎭
3. Не публикуйте незаконный контент🔞
4. Избегайте спама и рекламы📢

📝 Помните, что администрация бота имеет право изменять правила по своему усмотрению для обеспечения комфортного опыта для всех участников.""", reply_markup=nav.find_partner)
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
    dp.register_callback_query_handler(edit_questionnaire, text='edit_questionnaire')
    dp.register_message_handler(load_name, state=FSMWelcome.name)
    dp.register_message_handler(load_age, state=FSMWelcome.age)
    dp.register_message_handler(load_text, state=FSMWelcome.text)
    dp.register_callback_query_handler(load_gender_man, text='man', state=FSMWelcome.gender)
    dp.register_callback_query_handler(load_gender_woman, text='woman', state=FSMWelcome.gender)
