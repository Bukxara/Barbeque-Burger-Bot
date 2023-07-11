from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api import get_product_by_name, cart_of_user, get_product_by_id
from app import user_data


async def count_and_text(tg_id, product_name, num):
    # Quantity of product inline markup

    data = await get_product_by_name(product_name)
    product = data[0]              

    button = InlineKeyboardMarkup(
            inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="option_decr"),
            InlineKeyboardButton(text=num, callback_data="option_num"),
            InlineKeyboardButton(text="➕", callback_data="option_incr")
        ]
    ]
)
    text = f"""*{product["product_name"]}*
{product["product_description"]}\n
{product["product_name"]} | {product["product_price"]} x {num} = {product["product_price"]* num}\n"""
    
    drinks = [
        InlineKeyboardButton(text="Sprite", callback_data="option_sprite"),
        InlineKeyboardButton(text="Coca-Cola", callback_data="option_coca-cola"),
        InlineKeyboardButton(text="Fanta", callback_data="option_fanta")
    ]
    snacks = [
        InlineKeyboardButton(text="Potato Balls", callback_data="option_potato"),
        InlineKeyboardButton(text="French Fries", callback_data="option_fries"),
        InlineKeyboardButton(text="Country Style Potato", callback_data="option_country")
    ]
    kids = [
        InlineKeyboardButton(text="Мальчик", callback_data="option_boy"),
        InlineKeyboardButton(text="Девочка", callback_data="option_girl")
    ]

    if product["Drinks"]:
        if user_data[tg_id]["Напитки"]:
            product["Drinks"] = user_data[tg_id]["Напитки"]
        else:
            user_data[tg_id]["Напитки"] = product["Drinks"]
        button.add(InlineKeyboardButton(text="⬇️Напитки⬇️", callback_data="nothing"))

        for drink in drinks:
            if drink["text"] == product["Drinks"]:
                drink["text"] = "✅ " + drink["text"]
        button.row(*drinks)
        text += f"""Напитки:
    - {product["Drinks"]} {num} шт.\n"""
        
    if product["Snacks"]:
        if user_data[tg_id]["Снеки"]:
            product["Snacks"] = user_data[tg_id]["Снеки"]
        else:
            user_data[tg_id]["Снеки"] = product["Snacks"]
        button.add(InlineKeyboardButton(text="⬇️Снеки⬇️", callback_data="nothing"))

        for snack in snacks:
            if snack["text"] == product["Snacks"]:
                snack["text"] = "✅ " + snack["text"]
        button.row(*snacks)
        text += f"""Cнеки:
    - {product["Snacks"]} {num} шт.\n"""
        
    if product["Kids"]:
        if user_data[tg_id]["Kids Box"]:
            product["Kids"] = user_data[tg_id]["Kids Box"]
        else:
            user_data[tg_id]["Kids Box"] = product["Kids"]
        button.add(InlineKeyboardButton(text="⬇️Kids Box⬇️", callback_data="nothing"))
        
        for kid in kids:
            if kid["text"] == product["Kids"]:
                kid["text"] = "✅ " + kid["text"]
        button.row(*kids)
        text += f"""Kids box:
    - {product["Kids"]} {num} шт."""
        
    text += f'\nИтого: {product["product_price"]*num} UZS'
    

    button.add(InlineKeyboardButton(text="📥 Добавить в корзину", callback_data="option_add"))
    return {"button": button, "text": text}


async def cart_button(tg_id):
    # Making a cart button for a user

    button = InlineKeyboardMarkup(
            inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить заказ", callback_data="cart_confirm")
        ],
        [
            InlineKeyboardButton(text="Продолжить заказ", callback_data="cart_continue")
        ],
        [
            InlineKeyboardButton(text="🔄 Очистить", callback_data="cart_empty"),
        ]
    ], row_width=1
)
    products = await cart_of_user(tg_id)
    cart_text = ""
    product_items_text = ""
    total_price = 0

    for product in products:
        product_id = product["product_id"]
        food = await get_product_by_id(product_id)
        name = food["product_name"]
        quantity = product["product_quantity"]
        price = food["product_price"]

        cart_text += f"*{name}* x {quantity} = {price*quantity:,}\n"
        product_items_text += f"{name} x {quantity}\n"
        
        if product["product_options"]:
            for k,v in product["product_options"].items():
                cart_text += f"*{k}:*\n\t- {v} x {quantity}\n"
                product_items_text += f"{k}:\n\t - {v} x {quantity}\n"

        total_price += quantity*price
        button.row(*[
            InlineKeyboardButton(text="➖", callback_data=f"cart_decr_{product_id}"),
            InlineKeyboardButton(text=f"{name}", callback_data="cart_nothing"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_incr_{product_id}")
        ])

    price_text = f"*Итого:* {total_price:,} UZS"
    return {"cart_text": cart_text, "price_text": price_text, "product_items": product_items_text,
            "button": button, "is_empty": total_price < 300, 'total_price': total_price}


payment_method = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 Cash", callback_data="method_cash")
        ],
        [
            InlineKeyboardButton(text="💳 Click", callback_data="method_click"),
            InlineKeyboardButton(text="💳 Payme", callback_data="method_payme")
        ],
    ]
)


confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Отменить", callback_data="confirm_cancel")
        ],
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_confirm"),
            InlineKeyboardButton(text="🔄 Изменить", callback_data="confirm_change")
        ],
    ]
)

