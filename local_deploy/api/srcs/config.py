from pydantic import BaseSettings, BaseModel, PositiveInt

class CeleryConfig(BaseModel):
    broker_url: str
    result_backend: str | None = None


class Config(BaseSettings):
    postgres_url: str
    celery: CeleryConfig
    sentry_dsn: str | None = None
    uploads_location: str = '/uploads/'
    bucket_name: str | None = None
    api_url: str
    maximum_pending_ingestion_flows: PositiveInt = 5
    verbose_chains: bool = True

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


cfg = Config()

TORTOISE_ORM = {
    "connections": {
        "default": cfg.postgres_url
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "srcs.app.models",
                "srcs.tasks.models"
            ],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}
TORTOISE_MODULES = {"models": ["srcs.app.models", "srcs.tasks.models"]}
