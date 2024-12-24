from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    GOOGLE_API_KEY: str
    MODEL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env')

settings = Settings()