
from loader import dp
from .throttling import ThrottlingMiddleware
from loader import bot


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware(bot))
