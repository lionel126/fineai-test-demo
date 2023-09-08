from requests import request
import pytest
import face_recognition
from api.app import App
from api.config import settings


def test_compare():
    pics =  [
        '/Users/chensg/Downloads/60f6998a-3fd5-4bc0-9827-bae3312fea61.png',
        '/Users/chensg/Downloads/a41c6b26-1adf-45c3-b24d-38940b0badda.jpeg',
        # '/Users/chensg/Pictures/Alexandra Daddario/0457f991c5d17bde63a10a18ad56052a.jpg', 
        # '/Users/chensg/Pictures/Alexandra Daddario/1b7131abe7284690a1e349878a5eeaae.bmp',
        # '/Users/chensg/Pictures/Alexandra Daddario/6MM4MAHRVFMEPLJYQHVTH5WCPI.jpg'
    ]
    encodings = []
    for p in pics:
        im = face_recognition.load_image_file(p)
        encodings.append(face_recognition.face_encodings(im)[0])
    
    
    ret = face_recognition.compare_faces(encodings, encodings[0])
    print(f'{ret=}')
    distance = face_recognition.face_distance(encodings, encodings[0])
    print(f'{distance=}')

@pytest.mark.asyncio
async def test_yyy():
    # app = await App('c')
    app = await App(14)
    app.output_portray(modelId=401, themeId=1, themeModelId=1)


def test_zzz():
    app = App('c')
    # app = App(14)
    app.output_portray(modelId=401, themeId=1, themeModelId=1)

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