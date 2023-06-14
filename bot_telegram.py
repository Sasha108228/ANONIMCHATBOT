from aiogram.utils import executor
from create_bot import dp, bot

from handlers import *


async def on_startup(_):
	print('Бот вышел в онлайн')
	await bot.send_message(1030874842, 'Online')


check_subscribe.register_handlers_check_subscribe(dp)
welcome.register_handlers_welcome(dp)
# main.register_handlers_main(dp)
bot_mailling.register_handlers_bot_mailling(dp)
claim.register_handlers_claim(dp)
block.register_handlers_block(dp)
bot_mailling_keyboard1.register_handlers_bot_mailling_keyboard1(dp)
client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

