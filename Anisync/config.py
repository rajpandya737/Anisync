import os.path


# Flask config
HOST = "0.0.0.0"
PORT = 8000
DEBUG = False
ENV = "production"

# Anime list config
START = 0
END = 300
TEST_MODE = True

# Database config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "translated_anime_list.sqlite")