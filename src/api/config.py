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

    app_base_url: str = 'https://dev-wukm.vmovier.cc'
    internal_base_url: str = 'https://dev-wukm.vmovier.cc/internal/'
    task_base_url: str = 'http://10.173.36.244/api/v1/task/'
    http_proxy: str = ''
    https_proxy: str = ''
    REQUESTS_CA_BUNDLE: str = ''

    postgresql_uri_sync: str = 'postgresql+psycopg://appuser:4b9d46ebc@10.173.4.249:5432/app_store'

    user_info: dict[str, UserSetting] = {}

    def get_user_info(self, uid: str):
        return self.user_info.get(uid)

    # test data
    # pictures directory
    scarlett: str = '/Users/chensg/Pictures/scarlettJohansson'
    daddario: str = '/Users/chensg/Pictures/Alexandra Daddario'
    captain: str = '/Users/chensg/Pictures/americanCaptain'
    guoda: str = '/Users/chensg/Pictures/guoda'
    jason: str = '/Users/chensg/Pictures/JasonStatham'
    lf: str = '/Users/chensg/Pictures/lf_样本预处理/lf_train_pics'

    env: str = 'dev'
    token_key: str = 'USER-COOKIE-TOKEN-DEV'
    token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlvbklkIjoiZE1ZWm9FWDZkbE9yNVI3ayIsInN1YiI6IlhXIElUIENvLiIsImlzcyI6Imh0dHA6Ly9kZXYtd3VrbS52bW92aWVyLmNjIiwibG9naW5fdXNlcl9rZXkiOiJkNmFmYWM2OGY4OWViZDdkZmZjYTQ2YmY0N2M3MjdkMyJ9.IHbT8CuSraRKTXY9zrvtPbyOgrQ6zv_32vWNBxAv0UE'

    max_memory: int = 4

    loop_count: int = 50

settings = Settings()
