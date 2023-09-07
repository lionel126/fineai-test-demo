from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class UserSetting(BaseSettings):
    user_id: int
    id: int
    union_id: str
    openid: str
    app_id: str

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
    
    postgresql_uri_sync: str = 'postgresql+psycopg://appuser:4b9d46ebc@10.173.4.249:5432/app_store'
    
    user_info: dict[str, UserSetting] = {}

    def get_user_info(self, uid:str):
        return self.user_info.get(uid)


settings = Settings()
