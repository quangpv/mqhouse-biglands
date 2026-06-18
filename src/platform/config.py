from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BIGLANDS_", env_file=".env")

    app_name: str = "Biglands API"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5444/biglands"
    test_database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5445/biglands_test"
    database_echo: bool = False

    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours

    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10

    expiration_days: int = 30
    max_hot_items: int = 14

    log_level: str = "INFO"
    log_format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


settings = Settings()
