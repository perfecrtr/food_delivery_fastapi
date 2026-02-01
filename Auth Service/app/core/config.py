"""
    Config module for Auth Service
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Auth Service'

    db_host: str
    db_user: str
    db_port: int
    db_pass: str
    db_name: str

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

        @property
        def database_url(self) -> str:
            """Return full database URL"""
            return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
