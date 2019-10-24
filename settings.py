from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()
DB_PATH = Path.joinpath(ROOT_DIR, 'the_db.sqlite')
API_KEY_PATH = Path(ROOT_DIR, 'secure/api_key.txt')
OUTPUT_PATH = Path(ROOT_DIR, 'outputs')
