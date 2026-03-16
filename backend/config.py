from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8742
    host: str = "127.0.0.1"
    db_path: str = "local_biz_scraper.db"
    scrape_timeout: int = 10
    scrape_max_retries: int = 2
    scrape_concurrency: int = 5
    nominatim_user_agent: str = "local-biz-scraper/0.1.0"

    model_config = {"env_prefix": "LBS_"}


settings = Settings()
