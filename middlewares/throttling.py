import asyncio
from datetime import datetime, time

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        current_time = datetime.now().time()
        if not self.is_working_hours(current_time):
            await message.reply("Hozir men dam olmoqdaman 💤💤💤\nErtalab soat 10:00 dan ishga tushaman 😉😉😉")
            raise CancelHandler()

        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        if throttled.exceeded_count <= 4:
            await message.reply("Too many requests!")

    @staticmethod
    def is_working_hours(current_time):
        start_time_morning = time(10, 0)
        end_time_morning = time(23, 59)  # 11:59 PM

        start_time_night = time(0, 0)  # 12:00 AM
        end_time_night = time(3, 0)

        if start_time_morning <= current_time <= end_time_morning:
            return True
        elif start_time_night <= current_time <= end_time_night:
            return True
        return False

