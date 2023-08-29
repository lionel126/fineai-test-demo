import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="allow",
        str_strip_whitespace=True,
    )  # type: ignore

    app_base_url:str = 'https://dev-wukm.vmovier.cc'
    internal_base_url:str = 'https://dev-wukm.vmovier.cc/internal/'
    http_proxy:str = ''
    https_proxy:str = ''
    REQUESTS_CA_BUNDLE:str = ''


settings = Settings()
