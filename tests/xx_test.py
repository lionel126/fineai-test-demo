from requests import request
import pytest

from api.app import App
from api.config import settings


@pytest.mark.asyncio
async def test_yyy():
    # app = await App('c')
    app = await App(14)
    app.output_portray(modelId=401, themeId=1, themeModelId=1)

@pytest.mark.asyncio
async def test_xxx():
    li = [1]
    print(li * 5)

cert = settings.REQUESTS_CA_BUNDLE
proxies = {'http': settings.http_proxy, 'https': settings.https_proxy}

def test_mq():
    tasks = [
        '38563706-8d23-4748-9505-1cd2b29ee14c',
        '24176e75-f572-4424-9424-fedfeb6126a1',
        '671a6f05-c85f-4526-ab2c-6381b2e7ca4f'
    ]
    request('post', 'http://192.168.103.101:8000/consume', json=tasks, proxies=proxies, verify=cert)
    # consume(**json)