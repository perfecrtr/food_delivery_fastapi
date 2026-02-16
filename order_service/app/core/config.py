from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = 'Order Service'

    db_host: str = Field(..., env="DB_HOST")
    db_user: str = Field(..., env="DB_USER")
    db_port: int = Field(..., env="DB_PORT")
    db_pass: str = Field(..., env="DB_PASS")
    db_name: str = Field(..., env="DB_NAME")

    restaurant_service_url: str = "http://restaurant-service:8000/"

    services_timeout: int = 5
    service_max_retries: int = 3

    jwt_secret_key: str
    jwt_algorithm: str

    redis_host: str
    redis_port: int
    redis_password: str
    redis_db: int
    redis_ttl: int

    KAFKA_BOOTSTRAP_SERVERS: str 
    KAFKA_CLIENT_ID: str
    
    KAFKA_PRODUCER_ACKS: str
    KAFKA_PRODUCER_RETRIES: int
    KAFKA_PRODUCER_MAX_BLOCK_MS: int
    KAFKA_PRODUCER_COMPRESSION_TYPE: str

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