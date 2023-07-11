from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from json import dumps
from data.config import ADMINS
from states.states import Stages, Customer, Order, Others
from keyboards.default.reply import (locations_button, start, categories_button, products_by_category, product_button, 
                                     back, location_options, skip, main_menu, branches, settings, address_confirmation)
from keyboards.inline.inline import count_and_text, cart_button, payment_method, confirmation
from app import user_data
from api import (put_number, post_address, category_by_name, get_product_by_name, purchase_product, empty_cart, 
                 check_address, update_product_quantity, delete_product, post_order, last_order, leave_comment, 
                 get_orders_of_user, put_birthday, get_addresses, get_or_create_customer)
from data.config import URL_FOR_IMAGE
import re


@dp.message_handler(text="📥 Корзина", state="*")
async def cart(message: types.Message, state: FSMContext):
    # Cart of a user

    result = await cart_button(message.from_user.id)

    if result['is_empty']:
        await message.answer(text="Ваша корзина пусто!")
        markup = await categories_button()
        await message.answer("Выберите категорию", reply_markup=markup)
        await state.set_state(Stages.category)
    else:
        await message.answer(text="Корзина", reply_markup=back)
        await message.answer(text=f"{result['cart_text']}\n{result['price_text']}",
                             reply_markup=result["button"], parse_mode="Markdown")
        await state.set_state(Stages.cart)


@dp.message_handler(text="⬅️ Назад", state="*")
async def back_button_handler(message: types.Message, state: FSMContext):
    # Handling all the "⬅️ Назад" buttons

    current_state = await state.get_state()
    if current_state in [*Others.all_states_names, "Customer:location"]:
        await state.set_state(None)
        await message.answer("Для заказа нажмите 🛍 Заказать\n\nА также вы можете посмотреть акции и ознакомиться с местонахождением наших филиалов", reply_markup=start)
    
    elif current_state in ["Stages:product", "Stages:cart", *Order.all_states_names]:
        markup = await categories_button()
        await message.answer("Выберите категорию", reply_markup=markup)
        await state.set_state(Stages.category)

    elif current_state == "Stages:quantity":
        data = await state.get_data()
        markup = await products_by_category(data["category"])
        await message.answer(f"{data['category']}\n\nВыберите продукт",
                             reply_markup=markup)
        user_data[message.from_user.id]["num"] = 1
        await state.set_state(Stages.product)

    elif current_state in ["Stages:category", "Customer:customers_addresses", "Customer:address_confirmation", "Customer:customers_addresses"]:
        await message.answer("Чтобы продолжить заказ, пожалуйста выберите один из опций", reply_markup=location_options)
        await state.set_state(Customer.location)

    elif current_state == None:
        await message.answer("Для заказа нажмите 🛍 Заказать\n\nА также вы можете посмотреть акции и ознакомиться с местонахождением наших филиалов", reply_markup=start)



@dp.message_handler(content_types="contact", state=Customer.phone)
async def number_handler(message: types.Message, state: FSMContext):
    # Updating user's phone number

    await put_number(message.from_user.id, message.contact.phone_number)
    await message.answer("Для заказа нажмите 🛍 Заказать\n\nА также вы можете посмотреть акции и ознакомиться с местонахождением наших филиалов", reply_markup=start)
    await state.finish()


@dp.message_handler(text="🛍 Заказать", state="*")
async def categories_view(message: types.Message, state: FSMContext):
    # Location markup view and setting state to the location

    user_data[message.from_user.id] = {}
    user_data[message.from_user.id].update(dict.fromkeys(["Напитки", "Снеки", "Kids Box"], ""))
    await message.answer("Чтобы продолжить заказ, пожалуйста выберите один из опций", reply_markup=location_options)
    await state.set_state(Customer.location)

@dp.message_handler(state=Customer.location)
async def location_handler(message: types.Message, state: FSMContext):
    # Providing user with 2 options
    
    if message.text == "🏠  Мои адреса":
        result = await locations_button(message.from_user.id)
        if result["is_empty"]:
            await message.answer("У вас ещё нет сохранённого адреса", reply_markup=result["button"])
        else:
            await message.answer("Выберите адрес", reply_markup=result["button"])
        await state.set_state(Customer.customers_addresses)

    else:
        return await message.reply("Пожалуйста выберите один из опций!")
    

@dp.message_handler(content_types="location", state=[Customer.location, Customer.address_confirmation])
async def location_sending(message: types.Message, state: FSMContext):
    # Checking one's location address
    
    address = await check_address(message.location)
    await state.update_data(address_coordinates=address["coordinates"], address_text=address["address"])
    await message.answer(f'Ваш адрес:\n📍 *{address["address"]}*\nПодтвердите адрес?', parse_mode="Markdown", reply_markup=address_confirmation)
    await state.set_state(Customer.address_confirmation)


@dp.message_handler(state=Customer.address_confirmation)
async def final_stage_location(message: types.Message, state: FSMContext):
    # Final stage of location sending
    
    if message.text == "✅ Подтвердить":
        markup = await categories_button()
        await message.answer("Выберите категорию", reply_markup=markup)
        await state.set_state(Stages.category)
    
    elif message.text == "Добавить в мои адреса":
        data = await state.get_data()
        users_addresses = await get_addresses(message.from_user.id)

        if data["address_text"] in [address["address_text"] for address in users_addresses]:
            return await message.answer("Вы уже добавили этот адрес")
        
        await post_address(message.from_user.id, data["address_coordinates"], data["address_text"])
        await message.answer("Ваша геопозиция успешно добавлена. Выберите один из опций", reply_markup=location_options)
        await state.set_state(Customer.location)

    else:
        return await message.reply("Пожалуйста выберите один из опций!")


@dp.message_handler(state=Customer.customers_addresses)
async def location_choice(message: types.Message, state: FSMContext):
    # Picking address from saved ones
    
    addresses = await get_addresses(message.from_user.id)
    if message.text not in [address["address_text"] for address in addresses]:
        return await message.answer("Выберите адрес")
    
    await state.update_data(address_text=message.text)
    markup = await categories_button()
    await message.answer("Выберите категорию", reply_markup=markup)
    await state.set_state(Stages.category)
    

@dp.message_handler(state=Stages.category)
async def products_view(message: types.Message, state: FSMContext):
    # Products markup view and setting state to the product

    data = await category_by_name(message.text)
    if data:
        await state.update_data(category=message.text)
        markup = await products_by_category(message.text)
        await message.answer(f"{message.text}\n\nВыберите продукт",
                             reply_markup=markup)
        await state.set_state(Stages.product)
    else:
        return await message.reply("Пожалуйста, выберите один из приведённых категорий!")


@dp.message_handler(state=Stages.product)
async def quantity_view(message: types.Message, state: FSMContext):
    # Quantity of product and adding different type of extra options to that button

    data = await get_product_by_name(message.text)
    if data:
        product = data[0]
        await state.update_data(product=message.text)
        result = await count_and_text(message.from_user.id, message.text, 1)
        markup = result["button"]
        text = result["text"]

        await message.answer("Выберите количество продукта", reply_markup=product_button)
        await message.answer_photo(photo=f'{URL_FOR_IMAGE}{product["product_image"]}',
                                   caption=text, parse_mode="Markdown", reply_markup=markup)
        user_data[message.from_user.id]["num"] = 1
        await state.set_state(Stages.quantity)
    else:
        return await message.reply("Пожалуйста, выберите один из приведённых продуктов!")


async def update_num_text(message: types.Message, product_name, new_value: int):
    with suppress(MessageNotModified):
        result = await count_and_text(message.chat.id, product_name, new_value)
        await message.edit_caption(result["text"], parse_mode="Markdown", reply_markup=result["button"])


@dp.callback_query_handler(Text(startswith="option_"), state=[Stages.quantity, "*"])
async def nums_callback(call: types.CallbackQuery, state: FSMContext):
    # Product purchase inline buttons settings

    product_options = {"sprite": "Sprite", "coca-cola": "Coca-Cola", "fanta": "Fanta",
                       "potato": "Potato Balls", "fries": "French Fries", "country": "Country Style Potato",
                       "boy": "Мальчик", "girl": "Девочка"}

    user_value = user_data.get(call.from_user.id, {}).get("num", 1)
    action = call.data.split("_")[1]
    info = await state.get_data()
    product_name = info["product"]

    if action == "incr":
        user_data[call.from_user.id]["num"] = user_value + 1
        await call.answer(f"{user_value + 1} шт.")
        await update_num_text(call.message, product_name, user_value + 1)

    elif action == "decr":
        if user_value > 1:
            user_data[call.from_user.id]["num"] = user_value - 1
            await call.answer(f"{user_value - 1} шт.")
            await update_num_text(call.message, product_name, user_value - 1)
        else:
            await call.answer(f"{user_value} шт.")

    elif action == "num":
        await call.answer(f"{user_value} шт.")

    elif action in ["sprite", "coca-cola", "fanta"]:
        user_data[call.from_user.id]["Напитки"] = product_options.get(
            action)
        await update_num_text(call.message, product_name, user_value)

    elif action in ["potato", "fries", "country"]:
        user_data[call.from_user.id]["Снеки"] = product_options.get(
            action)
        await update_num_text(call.message, product_name, user_value)

    elif action in ["boy", "girl"]:
        user_data[call.from_user.id]["Kids Box"] = product_options.get(action)
        await update_num_text(call.message, product_name, user_value)

    elif action == "add":
        options = {k: user_data[call.from_user.id][k] for k in user_data[call.from_user.id]
                   if user_data[call.from_user.id][k] and not isinstance(user_data[call.from_user.id][k], int)}
        await state.update_data(options=dumps(options))
        await state.update_data(quantity=user_value)
        async with state.proxy() as data:
            product = await get_product_by_name(data["product"])
            product_id = product[0]["id"]
            result = await purchase_product(call.from_user.id, product_id, data["quantity"], data["options"])
            markup = await categories_button()
            await call.answer(result)
            await call.message.delete()
            await call.message.answer("Выберите категорию", reply_markup=markup)
            
            user_data[call.from_user.id]["Напитки"], user_data[call.from_user.id][
                "Снеки"], user_data[call.from_user.id]["Kids Box"] = "", "", ""
        await state.set_state(Stages.category)

    await call.answer()


@dp.callback_query_handler(Text(startswith="cart_"), state=Stages.cart)
async def carts_callback(call: types.CallbackQuery, state: FSMContext):
    # Cart modification inline button
    action = call.data.split("_")[1]

    if action in ["continue", "empty"]:
        if action == "empty":
            result = await empty_cart(call.from_user.id)
            await call.answer(result)
            await call.message.delete()
        markup = await categories_button()
        await call.message.answer("Выберите категорию", reply_markup=markup)
        await state.set_state(Stages.category)

    elif action in ["incr", "decr"]:
        product_id = call.data.split("_")[2]
        data = await update_product_quantity(call.from_user.id, product_id)

        if action == "incr":
            await update_product_quantity(call.from_user.id, product_id, data["product_quantity"] + 1)

        else:
            if data["product_quantity"] == 1:
                await delete_product(call.from_user.id, product_id)
            await update_product_quantity(call.from_user.id, product_id, data["product_quantity"] - 1)

        result = await cart_button(call.from_user.id)

        if result['is_empty']:
            await call.message.answer(text="Ваша корзина пусто!")
            await call.message.delete()
            markup = await categories_button()
            await call.message.answer("Выберите категорию", reply_markup=markup)
            await state.set_state(Stages.category)
        else:
            await call.message.edit_text(f"{result['cart_text']}\n{result['price_text']}", parse_mode="Markdown", reply_markup=result["button"])

    elif action == "confirm":
        result = await cart_button(call.from_user.id)
        await state.update_data(text=f"{result['cart_text']}\n\n*Сумма доставки:* 10,000\n*Итого:* {result['total_price']+10000:,} UZS")
        await call.message.delete()
        data = await state.get_data()
        await call.message.answer(f"{data['text']}\n*Геолокация:* {data['address_text']}", parse_mode="Markdown", reply_markup=payment_method)
        await state.set_state(Order.payment_method)


@dp.callback_query_handler(Text(startswith="method"), state=Order.payment_method)
async def methods_callback(call: types.CallbackQuery, state: FSMContext):
    # Payment method choice 

    method = call.data.split("_")[1]
    data = await state.get_data()
    await state.update_data(payment_method=method.capitalize())
    await call.message.edit_text(f"{data['text']}\n*Геолокация:* {data['address_text']}\n*Тип оплаты:* 💳{method.capitalize()}", parse_mode="Markdown", reply_markup=confirmation)
    await state.set_state(Order.confirmation)


@dp.callback_query_handler(Text(startswith="confirm"), state=Order.confirmation)
async def confirmations_callback(call: types.CallbackQuery, state: FSMContext):
    # In case client changes his mind)

    confirmation = call.data.split("_")[1]
    data = await state.get_data()

    if confirmation == "change":
        await call.message.edit_text(f"{data['text']}\n{data['address_text']}", reply_markup=payment_method, parse_mode="Markdown")
        await state.set_state(Order.payment_method)
    
    elif confirmation == "cancel":
        await empty_cart(call.from_user.id)
        await call.message.answer("Для заказа нажмите 🛍 Заказать\n\nА также вы можете посмотреть акции и ознакомиться с местонахождением наших филиалов", reply_markup=start)
        await state.finish()
    
    elif confirmation == "confirm":
        await state.update_data(text = data["text"] + f"\n*Тип оплаты:* {data['payment_method']}")
        await call.message.answer("Оставьте комментарий к заказу.", reply_markup=skip)
        await state.set_state(Order.comment)


@dp.message_handler(state=Order.comment)
async def comment_stage(message: types.Message, state: FSMContext):
    # Last stage of ordering
    
    data = await state.get_data()
    result = await cart_button(message.from_user.id)

    if message.text != "Пропустить":
        await state.update_data(comment=message.text)
        await post_order(message.from_user.id, result["product_items"], data["payment_method"], 
                         data["address_text"], message.text, result["total_price"]+10000, "In progress")
    else:
        await post_order(message.from_user.id, result["product_items"], data["payment_method"], 
                         data["address_text"], "", result["total_price"]+10000, "In progress")
    
    await empty_cart(message.from_user.id)
    order = await last_order()
    await message.answer(data["text"], parse_mode="Markdown")
    await message.answer(f"Ваш заказ #{order[0]['id']}. Спасибо! Для подтверждения заказа в скором времени с Вами свяжется оператор.", reply_markup=main_menu)
    await state.finish()
    customer = await get_or_create_customer(message.from_user.first_name, message.from_user.username, message.from_user.id)

    for admin in ADMINS:
        await dp.bot.send_message(admin, f"""Новый заказ: *№ {order[0]['id']}*
Статус: *Новый*
Имя: *{message.from_user.first_name}*\n
*Номер:* {customer['phone_number']}\n
{result['cart_text']}\n
Тип оплаты: *{data['payment_method']}*\n
Локация: {data['address_text']}
Итого: *{result['total_price']+10000:,} UZS*
Комментарий: *{message.text}*""", parse_mode="Markdown")


@dp.message_handler(text="Главное меню", state="*")
async def afterorder(message: types.Message):
    # Getting back to main menu after order

    await message.answer("Для заказа нажмите 🛍 Заказать\n\nА также вы можете посмотреть акции и ознакомиться с местонахождением наших филиалов", reply_markup=start)


@dp.message_handler(text="🎉 Акция", state="*")
async def discount_info(message: types.Message, state: FSMContext):
    # Giving discount information to the client

    await message.answer_photo(photo=open("media/images/discount.jpg", "rb"), 
        caption="SET 500+\nПраздничные мини сеты 🔥\nSet 500+ с напитком объемом 0,5л на выбор 20,21,22", reply_markup=back)
    await state.set_state(Others.discount)


@dp.message_handler(text="✍️ Оставить отзыв", state="*")
async def asking_for_comment(message: types.Message, state: FSMContext):
    # as soon as leave a comment button is selected

    await message.answer("Оставьте свой отзыв. Нам важно ваше мнение.", reply_markup=back)
    await state.set_state(Others.comment)


@dp.message_handler(state=Others.comment)
async def taking_comment(message: types.Message, state: FSMContext):
    # Saving comment into database

    await leave_comment(message.from_user.id, message.text)
    await message.answer("✅ Ваш комментарий был принят")
    await message.answer("Для заказа нажмите 🛍 Заказать\n\nА также вы можете посмотреть акции и ознакомиться с местонахождением наших филиалов",reply_markup=start)
    await state.finish()


@dp.message_handler(text="🏘 Филиалы", state="*")
async def branches_info(message: types.Message, state: FSMContext):
    # Showing all the branches of BBQ

    await message.answer("Наши филиалы", reply_markup=branches)
    await state.set_state(Others.branches)


@dp.message_handler(text="📋 Мои заказы", state="*")
async def providing_5_orders(message: types.Message):
    # Getting 5 last orders of a user

    orders = await get_orders_of_user(message.from_user.id)
    
    if orders:
        for order in orders:
            await dp.bot.send_message(message.chat.id, f"""Номер заказа: {order['id']}\nСтатус: *{order['order_status']}*
Адрес: {order['order_address']}\n\n{order['order_items']}\n\nТип оплаты: *{order['payment_method']}*\n
Итого: *{order['order_sum']}* UZS""", parse_mode='Markdown')
    else:
        await message.answer("Вы всё ещё ничего не заказали", reply_markup=main_menu)


@dp.message_handler(text="ℹ️ О нас", state="*")
async def about_bbq_button(message: types.Message):
    # Providing info about BBQ Burger

    await message.answer_photo(photo=open("media/images/about.jpg", "rb"), caption='''
"Barbeque Burger" - Это первый в Ташкенте бургер
приготовленный на огне. Сочные котлеты приготовленные на огне в сочетании с отборными свежими овощами, создают
неповторимый вкус Barbeque Burger. А наша круглосуточная
доставка делает наши бургеры доступными в любое время.
Заказать доставку вы можете по телефонам: +998(71) 200 62 62''', reply_markup=back)


@dp.message_handler(text="⚙️ Настройки", state="*")
async def settings_options(message: types.Message, state: FSMContext):
    # Settings menu

    await message.answer("Выберите настройку", reply_markup=settings)
    await state.set_state(Others.settings)


@dp.message_handler(text="Добавить день рождения",state=Others.settings)
async def asking_for_birthday(message: types.Message, state: FSMContext):
    # Adding birthday option

    await message.answer("Введите свой день рождения в формате, похожем на «26-04-1999»", reply_markup=main_menu)
    await state.set_state(Others.birthday)


@dp.message_handler(state=Others.birthday)
async def fixing_birthday(message: types.Message, state: FSMContext):
    # Getting birthday of a user and adding it to db

    date_pattern = "^[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}$"
    match = re.match(date_pattern, message.text)
    if not match:
        await message.answer("Неправильный ввод!!!")
        return await message.answer("Введите свой день рождения в формате, похожем на «26-04-1999»")
    else:
        await message.answer("День рождения успешно добавлен.")
        await put_birthday(message.from_user.id, message.text)
        await state.finish()

