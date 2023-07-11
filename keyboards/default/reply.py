from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from api import all_categories, products_by_category_name, get_addresses


async def locations_button(telegram_id):
    # Getting user's addresses

    button = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button.insert(KeyboardButton(text="⬅️ Назад"))
    addresses = await get_addresses(telegram_id)
    for address in addresses:
        button.insert(KeyboardButton(text=address["address_text"]))
    
    return {"button": button, "is_empty": len(addresses)==0}


start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Заказать")
        ],
        [
            KeyboardButton(text="🎉 Акция"),
            KeyboardButton(text="✍️ Оставить отзыв")
        ],
        [
            KeyboardButton(text="🏘 Филиалы"),
            KeyboardButton(text="📋 Мои заказы")
        ],
        [
            KeyboardButton(text="ℹ️ О нас"),
            KeyboardButton(text="⚙️ Настройки")
        ],
    ], resize_keyboard=True
)


async def categories_button():
    # All categories button

    button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    categories = await all_categories()
    button.insert(KeyboardButton(text="⬅️ Назад"))
    button.insert(KeyboardButton(text="📥 Корзина"))

    for category in categories:
        button.insert(KeyboardButton(text=category["category_name"]))

    return button


async def products_by_category(category_name):
    # Products by category markup

    button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button.insert(KeyboardButton(text="⬅️ Назад"))
    button.insert(KeyboardButton(text="📥 Корзина"))
    
    
    products = await products_by_category_name(category_name)
 
    for product in products:
        button.insert(KeyboardButton(text=product["product_name"]))

    return button


product_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад"),
            KeyboardButton(text="📥 Корзина")
        ]
    ], resize_keyboard=True
)


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ], resize_keyboard=True
)


contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱 Мой номер", request_contact=True)
        ]
    ], resize_keyboard=True
)

location_options = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌍 Отправить мою геопозицию", request_location=True)
        ],
        [
            KeyboardButton(text="🏠  Мои адреса")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ],
    ], resize_keyboard=True
)


address_confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌍 Переотправить геопозицию", request_location=True),
            KeyboardButton(text="✅ Подтвердить")
        ],
        [
            KeyboardButton(text="Добавить в мои адреса"),
            KeyboardButton(text="⬅️ Назад")
        ],
    ], resize_keyboard=True
)


skip = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пропустить")
        ]
    ], resize_keyboard=True
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню")
        ]
    ], resize_keyboard=True
)


branches = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад"),
            KeyboardButton(text="BBQ Compas"),
        ],
        [
            KeyboardButton(text="BBQ Parus"),
            KeyboardButton(text="BBQ Chimgan"),
        ],
        [
            KeyboardButton(text="BBQ Samarqand Darvoza"),
            KeyboardButton(text="BBQ Minor"),
        ],
    ], resize_keyboard=True
)


settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить день рождения"),
            KeyboardButton(text="⬅️ Назад"),
        ]
    ], resize_keyboard=True
)

