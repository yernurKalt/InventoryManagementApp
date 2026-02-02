from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str
    model_config = SettingsConfigDict(env_file=".env")
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    WEBHOOK_URL: str

    @computed_field
    def DATABASE_URL(self) -> str:
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')
    
    @computed_field
    def SYNC_DATABASE_URL(self) -> str:
        return (f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    @computed_field
    def KEY(self) -> str:
        return f"{self.SECRET_KEY}"

    @computed_field
    def ALGORITHM(self) -> str:
        return f"{self.JWT_ALGORITHM}"

    @computed_field
    def EXPIRE_MINUTES(self) -> int:
        return self.ACCESS_TOKEN_EXPIRE_MINUTES

    @computed_field
    def REDIS_URL_VALUE(self) -> str:
        return self.REDIS_URL

    @computed_field
    def WEBHOOK_URL_VALUE(self) -> str:
        return self.WEBHOOK_URL


settings = Settings()