"""
    Config module for User Service
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = 'User Service'

    db_host: str = Field(..., env="DB_HOST")
    db_user: str = Field(..., env="DB_USER")
    db_port: int = Field(..., env="DB_PORT")
    db_pass: str = Field(..., env="DB_PASS")
    db_name: str = Field(..., env="DB_NAME")

    KAFKA_BOOTSTRAP_SERVERS: str 
    KAFKA_CLIENT_ID: str
    
    KAFKA_PRODUCER_ACKS: str
    KAFKA_PRODUCER_RETRIES: int
    KAFKA_PRODUCER_MAX_BLOCK_MS: int
    KAFKA_PRODUCER_COMPRESSION_TYPE: str
    KAFKA_CONSUMER_GROUP: str
    
    KAFKA_TOPIC_USER_REGISTERED: str 
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra="ignore"

    @property
    def database_url(self) -> str:
        """Return full database URL"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
settings = Settings()