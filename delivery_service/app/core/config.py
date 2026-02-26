from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Delivery Service"

    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_name: str = Field(..., env="DB_NAME")

    user_service_url: str = "http://user-service:8000/"

    services_timeout: int = 5
    service_max_retries: int = 3

    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(..., env="JWT_ALGORITHMS")

    kafka_bootstrap_servers: str = Field(..., env="KAFKA_BOOTSTRAP_SERVERS")
    kafka_client_id: str = Field(..., env="KAFKA_CLIENT_ID")

    class Config:
        env_file: str  =  ".env"
        env_file_encoding: str = "utf-8"
        case_sensitive: bool = False
        extra: str = "ignore"
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
settings = Settings()
