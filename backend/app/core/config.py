from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "Saurabh Shukla Technology Platform API"

    API_V1_PREFIX: str = "/api/v1"

    SQLALCHEMY_DATABASE_URI: str = (
        "mysql+pymysql://root:1234@127.0.0.1:3307/ss_platforms"
    )

    SECRET_KEY: str = "change-this-to-a-long-random-secret-key"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CORS_ORIGINS: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()