import uuid

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

__all__ = ["settings", "BucketSetting"]


class BucketSetting(BaseSettings):
    endpoint: str
    access_key: str
    secret_key: str
    addressing_style: str = "path"
    signature_version: str = "s3v4"


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="allow",
        str_strip_whitespace=True,
    )  # type: ignore

    postgresql_uri:str = 'postgresql+asyncpg://appuser:4b9d46ebc@10.173.4.249:5432/app_store'
    sql_echo:bool = True



settings = Settings()
