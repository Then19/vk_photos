from pydantic import BaseSettings


class Settings(BaseSettings):
    clickhouse_dsn: str


settings = Settings()
