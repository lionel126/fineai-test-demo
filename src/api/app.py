import requests
from requests.models import Response
from urllib.parse import urljoin, urlparse

from fineai_test.utils.utils import jwt_token


class Session(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url
    
    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs) -> Response:
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)

class App():
    
    def __init__(self, base_url):
        # s = requests.Session()
        s = Session(base_url)
        # s.proxies = proxies
        # s.verify = cert
        self.s = s
        self._login()

    def _login(self):
        url = urlparse(self.s.base_url)
        # iss = f'{url.scheme}://{url.hostname}'
        iss = f'http://{url.hostname}'
        self.s.cookies.update({'USER-COOKIE-TOKEN-DEV': jwt_token(iss)})
    
    def create_model(self):
        return self.s.post('/app/user/model/create')
    
    def create_face(self, json):
        return self.s.post('/app/user/model/face/create', json=json) 
    
    def finish_face(self, json):
        '''{
            "imageId":2,
            "modelId":1
        }'''
        return self.s.post('/app/user/model/image/face/finish', json=json)
    
    def job_state(self, job_id):
        return self.s.get(f'/app/user/model/job/state/{job_id}')

    def create_dataset(self, model_id, json):
        '''["a.jpg","b.png"]'''
        url = '/app/user/model/dataset/create'
        if model_id:
            url += f'?modelId={model_id}'
        return self.s.post(url, json=json) 
    
    def finish_dataset(self, model_id, ids):
        '''uploadIds: [1, 2, 3] '''
        url = '/app/user/model/image/dataset/finish'
        if model_id:
            url += f'?modelId={model_id}'
        return self.s.post(url, json=ids)


def upload(file, url, data):
    with open(file, 'rb') as f:
        requests.post(url, data=data, files={data['key']:f})