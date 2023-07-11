from aiogram.dispatcher.filters.state import State, StatesGroup


class Stages(StatesGroup):

    category = State()  # Category selection Stage
    product = State()  # Product selection Stage
    quantity = State()  # Quantity of product selection Stage
    cart = State()  # Whatever needs to be done with cart Stage


class Customer(StatesGroup):

    phone = State()
    location = State()
    customers_addresses = State()
    send_location = State()
    address_confirmation = State()
    

class Order(StatesGroup):

    phone = State()
    location = State()
    payment_method = State()
    confirmation = State()
    comment = State()


class Others(StatesGroup):

    discount = State()
    comment = State()
    branches = State()
    about = State()
    settings = State()
    birthday = State()
