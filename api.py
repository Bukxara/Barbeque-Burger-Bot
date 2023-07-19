from geopy.geocoders import Nominatim
from aiohttp import ClientSession
from data import config


url = config.URL
head = {"Authorization": f"token {config.MY_TOKEN}"}


async def get_or_create_customer(first_name, username, tg_id):
    # Checking if specific user exists in database, if not adding customer to the database

    async with ClientSession() as sessions:
        http = f"{url}/user/{tg_id}/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


    async with ClientSession() as sessions:
        http = f"{url}/customers/"
        async with sessions.post(http, data={
            "first_name": first_name,
            "username": username,
            "telegram_id": tg_id
        }, headers=head):
            return "Пользователь добавлен!"


async def all_categories():
    # Getting all categories as a JSON

    async with ClientSession() as sessions:
        http = f"{url}/categories/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


async def category_by_name(category_name):
    # Getting one specific category

    async with ClientSession() as sessions:
        http = f"{url}/filter/category/by-name/{category_name}/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


async def products_by_category_name(category_name):
    # Filtering products by category name

    async with ClientSession() as sessions:
        http = f"{url}/filter/products/by-category/{category_name}/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


async def get_product_by_name(product_name):
    # Getting one specific product by its name :)

    async with ClientSession() as sessions:
        http = f"{url}/filter/product/by-name/{product_name}"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


async def get_product_by_id(num):
    # Getting one specific product by its ID :]

    async with ClientSession() as sessions:
        http = f"{url}/products/{num}"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


async def purchase_product(tg_id, product_id, quantity, options):
    # Buying product and adding it to cart

    async with ClientSession() as sessions:
        http = f"{url}/cart/{tg_id}/{product_id}/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                async with sessions.put(http, data={
                    "product_quantity": quantity,
                    "product_options": options
                }):
                    return "Обновлено"
            else:
                http = f"{url}/carts/"
                async with sessions.post(http, data={
                    "customer": tg_id,
                    "product_id": product_id,
                    "product_quantity": quantity,
                    "product_options": options
                }, headers=head):
                    return "✅ Добавлено в корзину!"


async def update_product_quantity(tg_id, product_id, quantity=None, options=None):
    # Changing the quantity of a product

    async with ClientSession() as sessions:
        http = f"{url}/cart/{tg_id}/{product_id}/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                if not quantity:
                    return await data.json()
                else:
                    async with sessions.put(http, data={
                        "product_quantity": quantity,
                        "product_options": options
                    }, headers=head):
                        return "Обновлено"


async def cart_of_user(tg_id):
    # Getting cart of a user by it telegram ID

    async with ClientSession() as sessions:
        http = f"{url}/cart/{tg_id}/"
        async with sessions.get(http, headers=head) as data:
            if data.status == 200:
                return await data.json()


async def empty_cart(tg_id):
    # Clearing user's cart

    async with ClientSession() as sessions:
        http = f"{url}/cart/{tg_id}/"
        async with sessions.delete(http, headers=head):
            return "Ваша корзинка очищена!"


async def delete_product(tg_id, product_id):
    # Deleting one product from the cart

    async with ClientSession() as sessions:
        http = f"{url}/cart/{tg_id}/{product_id}/"
        async with sessions.delete(http, headers=head):
            return "Удалено!"


async def put_number(tg_id, number):
    # update user's phone number

    async with ClientSession() as sessions:
        http = f"{url}/user/{tg_id}/"
        async with sessions.put(http, data={
            "phone_number": number
        }, headers=head):
            return "Обновлено"


async def post_order(telegram_id, products, method, address, comment, order_sum, status):
    # Posting order to database

    async with ClientSession() as session:
        http = f"{url}/orders/"
        async with session.post(http, data={
            "customer": telegram_id,
            "items": products,
            "payment_method": method,
            "address": address,
            "comment": comment,
            "sum": order_sum,
            "status": status
        }, headers=head):
            return "Успешно заказано!"


async def all_orders():
    # Getting all orders from database

    async with ClientSession() as session:
        http = f"{url}/orders/"
        async with session.get(http, headers=head) as data:
            return await data.json()


async def last_order():
    # Getting only last order

    async with ClientSession() as session:
        http = f"{url}/last-order/"
        async with session.get(http, headers=head) as data:
            return await data.json()
        

async def leave_comment(tg_id, comment):
    async with ClientSession() as session:
        http = f"{url}/comment/"
        async with session.post(http, data={
            "customer": tg_id,
            "comment": comment
        }, headers=head):
            return "Благодарим за отзыв!"
        

async def get_orders_of_user(tg_id):
    # Get the last 5 orders of user by it telegram ID

    async with ClientSession() as session:
        http = f"{url}/filter/orders/{tg_id}/"
        async with session.get(http, headers=head) as data:
            return await data.json()


async def put_birthday(tg_id, birthday):
    # update user's birthday

    async with ClientSession() as sessions:
        http = f"{url}/user/{tg_id}/"
        async with sessions.put(http, data={
            "birthday": '-'.join(birthday.split('-')[::-1])
        }, headers=head):
            return "Обновлено"
        

async def get_addresses(tg_id):
    # Get all addresses of a user

    async with ClientSession() as sessions:
        http = f"{url}/filter/address/{tg_id}/"
        async with sessions.get(http, headers=head) as data:
            return await data.json()


async def check_address(coordinates):
    # Checking address by its coordinates

    geolocator = Nominatim(user_agent="bbq")
    latitude, longitude = str(coordinates.latitude), str(coordinates.longitude)
    data = geolocator.reverse(f"{latitude}, {longitude}")
    location_data = str(data).split(',')[:-2]
    address_text = ','.join(location_data)

    return {"coordinates": coordinates, "address": address_text}


async def post_address(telegram_id, coordinates, address_text):
    # Posting an address for a user

    async with ClientSession() as session:
        http = f"{url}/addresses/"
        async with session.post(http, data={
            "customer": telegram_id,
            "address_coordinates": coordinates,
            "address_text": address_text
        }, headers=head):
            return "Добавлено!"
