from aiogram import executor

from loader import dp, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from middlewares.throttling import ThrottlingMiddleware


throttling_middleware = ThrottlingMiddleware(bot)
dp.middleware.setup(throttling_middleware)

async def on_startup(dispatcher):
    
    # Basic commands (/star & /help)
    await set_default_commands(dispatcher)

    # Notification about initialization of the bot to admins
    await on_startup_notify(dispatcher)

user_data = {}


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)