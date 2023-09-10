import ssl
from functools import partial
from typing import Any
from aiohttp.client import _RequestContextManager
from aiohttp.typedefs import StrOrURL
import requests
import aiohttp
from urllib.parse import urljoin
from .config import settings


class Session(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()
        if not base_url:
            base_url = ''
        self.base_url = base_url

    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs) -> requests.Response:
        joined_url = urljoin(self.base_url, url)
        cert = settings.REQUESTS_CA_BUNDLE
        proxies = {'http': settings.http_proxy, 'https': settings.https_proxy}
        return super().request(method, joined_url, *args, verify=cert, proxies=proxies, **kwargs)

# class AsyncSession(aiohttp.ClientSession):
#     def __init__(self, base_url=None):
#         ssl_ctx = ssl.create_default_context(cafile=settings.REQUESTS_CA_BUNDLE)
#         conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
#         super().__init__(connector=conn)
#         if not base_url:
#             base_url = ''
#         self.base_url = base_url
    
#     async def _request(self, method: str, url: StrOrURL, **kwargs: Any) -> _RequestContextManager:
#         joined_url = urljoin(self.base_url, url)
#         return await super()._request(method, joined_url, proxy=settings.http_proxy, **kwargs)
    
class AsyncSession():
    def __init__(self, base_url=None):
        conn = None
        if settings.REQUESTS_CA_BUNDLE:
            ssl_ctx = ssl.create_default_context(cafile=settings.REQUESTS_CA_BUNDLE)
            conn = aiohttp.TCPConnector(ssl=ssl_ctx)
        s = aiohttp.ClientSession(connector=conn)
        if not base_url:
            base_url = ''
        self.base_url = base_url
        self.s = s
        self.cookie_jar = self.s.cookie_jar

    # async def __aenter__(self):
    #     return self

    # async def __aexit__(self):
    #     await self.s.close()
    async def close(self):
        await self.s.close()

    async def _request(self, method: str, url: StrOrURL, **kwargs: Any) -> _RequestContextManager:
        joined_url = urljoin(self.base_url, url)
        return await self.s.request(method, joined_url, proxy=settings.http_proxy, **kwargs)
    
    def __getattr__(self, __name: str) -> Any:
        if __name in ('get', 'post', 'put', 'delete', 'head', 'options', 'patch'):
            return partial(self._request, __name)
