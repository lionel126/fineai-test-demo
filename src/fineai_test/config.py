import logging
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

__all__ = ["settings", "BucketSetting"]


class BucketSetting(BaseSettings):
    endpoint: str
    access_key: str
    secret_key: str
    addressing_style: str = "path"
    signature_version: str = "s3v4"

class UserSetting(BaseSettings):
    user_id: int
    user_info_id: int
    union_id: str
    open_id: str
    app_id: str
    
class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="allow",
        str_strip_whitespace=True,
    )  # type: ignore

    postgresql_uri:str = 'postgresql+asyncpg://appuser:4b9d46ebc@10.173.4.249:5432/app_store'
    sql_echo:bool = True

    bucket: dict[str, dict[str, BucketSetting]] = {}

    def get_bucket(self, vendor: str, region: str) -> BucketSetting | None:
        return self.bucket.get(vendor, {}).get(region)

    usr: dict[str, UserSetting] = {}

    def get_usr(self, uid:str):
        return self.usr.get(uid)
    
    log_level: int = logging.DEBUG

settings = Settings()
