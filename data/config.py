from environs import Env

# environs kutubxonasidan  foydalanish
env = Env()
env.read_env()

# reading these from .env file
BOT_TOKEN = env.str("BOT_TOKEN")  # BOT TOKEN
ADMINS = env.list("ADMINS")  # List of ADMINs
# IP = env.str("ip")  # Host IP-address
MY_TOKEN = env.str("MY_TOKEN")
URL = env.str("URL")
URL_FOR_IMAGES = env.str("URL_FOR_IMAGES")