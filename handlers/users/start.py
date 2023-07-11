from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from api import get_or_create_customer
from keyboards.default.reply import start, contact
from app import user_data
from states.states import Customer

from loader import dp



@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    # Very first step towards our bot :]

    first_name, username, telegram_id = message.from_user.first_name, message.from_user.username, message.from_user.id
    await get_or_create_customer(first_name, username, telegram_id)
    await message.answer("Здравствтуйте! Добро пожаловать в наш бот!\nПожалуйста введите свой номер телефона\n\nОтправить номер можете с помощью кнопки *Мой номер*",
                         parse_mode="Markdown", reply_markup=contact)
    await state.set_state(Customer.phone)
    


