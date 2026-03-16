from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8742
    host: str = "127.0.0.1"
    db_path: str = "local_biz_scraper.db"
    database_url: str = ""
    allowed_origins: str = "*"
    scrape_timeout: int = 10
    scrape_max_retries: int = 2
    scrape_concurrency: int = 5
    nominatim_user_agent: str = "local-biz-scraper/0.1.0"

    model_config = {"env_prefix": "LBS_"}

    @property
    def effective_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"sqlite:///{self.db_path}"

    @property
    def is_sqlite(self) -> bool:
        return self.effective_database_url.startswith("sqlite")

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


settings = Settings()
