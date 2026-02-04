"""
    Config module for Auth Service
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Auth Service'

    db_host: str
    db_user: str
    db_port: int
    db_pass: str
    db_name: str

    redis_host: str
    redis_port: int
    redis_password: str
    redis_db: int
    redis_ttl: int

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    KAFKA_BOOTSTRAP_SERVERS: str 
    KAFKA_CLIENT_ID: str
    
    KAFKA_PRODUCER_ACKS: str
    KAFKA_PRODUCER_RETRIES: int
    KAFKA_PRODUCER_MAX_BLOCK_MS: int
    KAFKA_PRODUCER_COMPRESSION_TYPE: str
    
    KAFKA_TOPIC_USER_REGISTERED: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Return full database URL"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def redis_url(self) -> str:
        """Return full redis url"""
        return f"redis://{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
settings = Settings()