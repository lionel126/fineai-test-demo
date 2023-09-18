import ssl
import aiohttp
import asyncio
import aiofiles
from urllib.parse import urlparse
from .utils import jwt_token
from .session import AsyncSession
from .config import settings
from fineai_test.services.app import get_user_info


class AsyncObj():
    async def __new__(cls, *a, **kw):
        inst = super().__new__(cls)
        await inst.__init__(*a, **kw)
        return inst


class App(AsyncObj):

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.s.close()

    # async class implementation. Instantiate with: await App()
    async def __init__(self, uid: str | int | None = None, base_url=settings.app_base_url):

        s = AsyncSession(base_url)
        self.s = s
        self.base_url = base_url
        if uid:
            await self._login(uid)

    async def _login(self, uid: str | int):
        url = urlparse(self.base_url)
        # iss = f'{url.scheme}://{url.hostname}'
        iss = f'http://{url.hostname}' + (f':{url.port}' if url.port else '')
        # port: 80 in request header host on prod
        if settings.env == 'prod':
            # iss = f'https://{url.hostname}:80'
            # iss = f'http://{url.hostname}:9090'
            iss = f'{url.scheme}://{url.hostname}:{url.port if url.port else 80}'
        if isinstance(uid, str):
            user = settings.get_user_info(uid)
        else:
            user = await get_user_info(uid)
        self.s.cookie_jar.update_cookies(
            {settings.token_key: jwt_token(user, iss)})

    async def create_model(self):
        return await self.s.post('/app/user/model/create')
    
    async def face_list(self, model_id):
        return await self.s.get(f'/app/user/model/face/image/list?modelId={model_id}')

    async def dataset_list(self, model_id):
        return await self.s.get(f'/app/user/model/dataset/image/list?modelId={model_id}')

    async def create_face(self, json):
        '''json: default = {
            "modelId": 0, 
            "fileName": ""
        }
        '''
        return await self.s.post('/app/user/model/face/create', json=json)

    async def finish_face(self, json):
        '''{
            "imageId":2,
            "modelId":1
        }'''
        return await self.s.post('/app/user/model/image/face/finish', json=json)

    async def job_state(self, job_id):
        return await self.s.get(f'/app/user/model/job/state/{job_id}')

    async def create_dataset(self, model_id: int, json: dict):
        '''["a.jpg","b.png"]'''
        url = '/app/user/model/dataset/create'
        if model_id:
            url += f'?modelId={model_id}'
        return await self.s.post(url, json=json)

    async def finish_dataset(self, model_id: int, ids: list):
        '''uploadIds: [1, 2, 3] '''
        url = '/app/user/model/image/dataset/finish'
        if model_id:
            url += f'?modelId={model_id}'
        return await self.s.post(url, json=ids)

    async def update_model(self, json=None, **kw):
        '''json: default = {
                "birthday": "2014-09-01",
                "gender": "female",
                "id": 0,
                "modelName": "Daddario"
            }
        '''
        if json is None:
            json = {
                "birthday": "2014-09-01",
                "gender": "female",
                "id": 0,
                "modelName": "Daddario"
            }
        if kw:
            json.update(kw)
        path = '/app/user/model/update'
        return await self.s.post(path, json=json)

    async def train(self, model_id: int, params=None):
        path = f'app/user/model/train/{model_id}'
        return await self.s.post(path, params=params)

    async def theme_list(self):
        path = '/app/theme/list'
        return await self.s.get(path)

    async def theme_detail(self, theme_id):
        path = f'/app/theme/detail/{theme_id}'
        return await self.s.get(path)

    async def output_portray(self, json=None, params=None, **kw):
        '''json: default = {
            "modelId": 0,
            "themeId": 0,
            "themeModelId": 0
        }'''
        if json is None:
            json = {
                "modelId": 0,
                "themeId": 0,
                "themeModelId": 0
            }
        json.update(kw)
        path = '/app/image/output/portray'
        return await self.s.post(path, params=params, json=json)

    async def template_list(self):
        path = '/app/template/list'
        return await self.s.get(path)

    async def subscribe(self):
        '''need to call wx api first, then call server. or wont manage to send notification 
        json: {
            "key": "9ce51182-eb1a-479d-8a13-b00fc01c2e65",
            "location": "image",
            "templateId": "UG_tzP8x-STvlGEZCIXVxI_ZBLYendyZXgCLCm6wpkM"
        }'''

    async def create_order(self, json=None, **kw):
        '''
        :param json: default {
            "modelId": 0,
            "price": 1,
            "productId": "pum001",
            "productType": "user-model-pay"
        }
        '''
        path = '/app/order/create'
        if json is None:
            json = {
                "modelId": 0,
                "price": 1,
                "productId": "pum001",
                "productType": "user-model-pay"
            }
        json.update(kw)
        return await self.s.post(path, json=json)


async def uploads(fs):
    ssl_ctx = ssl.create_default_context(cafile=settings.REQUESTS_CA_BUNDLE)
    conn = aiohttp.TCPConnector(ssl=ssl_ctx)
    async with aiohttp.ClientSession(connector=conn) as s:
        tasks = [upload(s, f['fileName'], f['host'], f['uploadParam'])
                 for f in fs]
        # for f in fs:
        #     await upload(s, f['fileName'], f['host'], f['uploadParam'])
        ret = await asyncio.gather(*tasks, return_exceptions=True)
    return ret


async def upload(s: aiohttp.ClientSession, file: str, url: str, data: dict):
    async with aiofiles.open(file, 'rb') as f:
        file = {data['key']: await f.read()}
        data.update(file)
        res = await s.post(url, data=data, proxy=settings.http_proxy)
    return res
