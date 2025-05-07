from pathlib import Path
from pydantic_settings import BaseSettings
import aiosqlite

DB_NAME = "FastAPILearn"
DB_PATH = Path(__file__).parent
DB_URl = f'sqlite+aiosqlite:///{DB_PATH}/{DB_NAME}.db'
ECHO = True

class Settings(BaseSettings):
    db_name: str = DB_NAME
    db_url: str = DB_URl
    echo: bool = ECHO




settings = Settings()


