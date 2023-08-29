import requests
from urllib.parse import urljoin
from .config import settings

class Session(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()
        if not base_url:
            base_url = settings.app_base_url
        self.base_url = base_url
    
    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs) -> requests.Response:
        joined_url = urljoin(self.base_url, url)
        cert = settings.REQUESTS_CA_BUNDLE
        proxies = {'http': settings.http_proxy, 'https': settings.https_proxy}
        return super().request(method, joined_url, *args, verify=cert, proxies=proxies, **kwargs)