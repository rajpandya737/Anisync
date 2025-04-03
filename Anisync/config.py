import os.path
from datetime import timedelta

import dotenv

TEST_MODE = True

# Flask config
HOST = "0.0.0.0"
PORT = 8000
DEBUG = TEST_MODE
SESSION_LIFETIME = timedelta(days=1)

# Loads the secret key if it exists, otherwise uses a local host secret key
# To any hackers reading this, this is not the secret key I use for production
dotenv_path = os.path.join(os.path.dirname(__file__), "instance", ".env")
dotenv.load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    SECRET_KEY = "Local Host Secret Key"

# Anime list config
START = 0
END = 300


# Database config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "translated_anime_list.sqlite")
