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
            KeyboardButton(text="🍴 Menyu")
        ],
        [
            KeyboardButton(text="🎉 Aksiya"),
            KeyboardButton(text="✍️ Sharh qoldirish")
        ],
        [
            KeyboardButton(text="🏘 Bizning filiallarimiz"),
            KeyboardButton(text="📋 Mening buyurtmalarim")
        ],
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ],
    ], resize_keyboard=True
)


async def categories_button():
    # All categories button

    button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    categories = await all_categories()
    button.insert(KeyboardButton(text="⬅️ Orqaga"))
    button.insert(KeyboardButton(text="🛒 Savat"))

    for category in categories:
        button.insert(KeyboardButton(text=category["category_name"]))

    return button


async def products_by_category(category_name):
    # Products by category markup

    button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button.insert(KeyboardButton(text="⬅️ Orqaga"))
    button.insert(KeyboardButton(text="🛒 Savat"))
    
    
    products = await products_by_category_name(category_name)
 
    for product in products:
        button.insert(KeyboardButton(text=product["product_name"]))

    return button


product_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Orqaga"),
            KeyboardButton(text="🛒 Savat")
        ]
    ], resize_keyboard=True
)


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Orqaga")
        ]
    ], resize_keyboard=True
)


contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱 Mening raqamim", request_contact=True)
        ]
    ], resize_keyboard=True
)

location_options = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌍 Joylashuvni yuborish", request_location=True)
        ],
        [
            KeyboardButton(text="🏠 Mening manzillarim")
        ],
        [
            KeyboardButton(text="⬅️ Orqaga")
        ],
    ], resize_keyboard=True
)


address_confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌍 Joylashuvni qayta yuborish", request_location=True),
            KeyboardButton(text="✅ Tasdiqlash")
        ],
        [
            KeyboardButton(text="Mening manzillarimga qo'shing"),
            KeyboardButton(text="⬅️ Orqaga")
        ],
    ], resize_keyboard=True
)


skip = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Oʻtkazib yuborish")
        ]
    ], resize_keyboard=True
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Asosiy menyu")
        ]
    ], resize_keyboard=True
)


branches = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Orqaga"),
            KeyboardButton(text="Non kabob Compas"),
        ],
        [
            KeyboardButton(text="Non kabob Parus"),
            KeyboardButton(text="Non kabob Chimgan"),
        ],
        [
            KeyboardButton(text="Non kabob Samarqand Darvoza"),
            KeyboardButton(text="Non kabob Minor"),
        ],
    ], resize_keyboard=True
)


settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tug'ilgan kunni qo'shing"),
            KeyboardButton(text="⬅️ Orqaga"),
        ]
    ], resize_keyboard=True
)

