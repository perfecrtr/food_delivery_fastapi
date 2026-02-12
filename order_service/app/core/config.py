from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = 'Order Service'

    db_host: str = Field(..., env="ORDER_DB_HOST")
    db_user: str = Field(..., env="ORDER_DB_USER")
    db_port: int = Field(..., env="ORDER_DB_PORT")
    db_pass: str = Field(..., env="ORDER_DB_PASS")
    db_name: str = Field(..., env="ORDER_DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensititve = False
        extra = "ignore"

    @property
    def database_url(self) -> str:
        """Return full database URL"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
settings = Settings()