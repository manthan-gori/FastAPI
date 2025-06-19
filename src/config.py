from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    MAIL_USERNAME : str
    MAIL_PASSWORD : str
    MAIL_FROM : str
    MAIL_PORT : int
    MAIL_SERVER : str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS : bool = True
    MAIL_SSL_TLS : bool = False
    USE_CREDENTIALS : bool = True
    VALIDATE_CERTS : bool = True


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()