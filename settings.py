from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()
DB_PATH = Path.joinpath(ROOT_DIR, 'the_db.sqlite')
API_KEY_PATH = Path(ROOT_DIR, 'secure', 'api_key.txt')
OUTPUT_PATH = Path(ROOT_DIR, 'outputs')
MONGO_CONNECTION_STRING_PATH = Path(ROOT_DIR, 'secure', 'mongo_connection_string.txt')
CLIENT_SECRET_PATH = Path(ROOT_DIR, 'secure', 'client_secret.json')
USE_OAUTH = False
LESS_TRANSACTIONS = True  # makes bulk inserts asserting uniqueness default = True
