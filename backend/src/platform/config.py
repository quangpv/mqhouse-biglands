from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")

    app_name: str = "Biglands API"
    debug: bool = False

    db_host: str = "localhost"
    db_port: int = 5444
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "biglands"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    test_database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5445/biglands_test"
    database_echo: bool = False

    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10

    expiration_days: int = 30
    max_hot_items: int = 14

    log_level: str = "INFO"
    log_format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    log_dir: str = "/app/logs"


settings = Settings()
