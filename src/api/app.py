from urllib.parse import urlparse

from fineai_test.utils.utils import jwt_token
from .session import Session
from .config import settings

class App():
    
    def __init__(self, uid:str|None=None, base_url=settings.app_base_url):
        # s = requests.Session()
        s = Session(base_url)
        # s.proxies = proxies
        # s.verify = cert
        self.s = s
        if uid:
            self._login(uid)

    def _login(self, uid):
        url = urlparse(self.s.base_url)
        # iss = f'{url.scheme}://{url.hostname}'
        iss = f'http://{url.hostname}' + (f':{url.port}' if url.port else '')
        self.s.cookies.update({'USER-COOKIE-TOKEN-DEV': jwt_token(uid, iss)})
    
    def create_model(self):
        return self.s.post('/app/user/model/create')
    
    def create_face(self, json):
        '''json: default = {
            "modelId": 0, 
            "fileName": ""
        }
        '''
        return self.s.post('/app/user/model/face/create', json=json) 
    
    def finish_face(self, json):
        '''{
            "imageId":2,
            "modelId":1
        }'''
        return self.s.post('/app/user/model/image/face/finish', json=json)
    
    def job_state(self, job_id):
        return self.s.get(f'/app/user/model/job/state/{job_id}')

    def create_dataset(self, model_id:int, json:dict):
        '''["a.jpg","b.png"]'''
        url = '/app/user/model/dataset/create'
        if model_id:
            url += f'?modelId={model_id}'
        return self.s.post(url, json=json) 
    
    def finish_dataset(self, model_id:int, ids:list):
        '''uploadIds: [1, 2, 3] '''
        url = '/app/user/model/image/dataset/finish'
        if model_id:
            url += f'?modelId={model_id}'
        return self.s.post(url, json=ids)
    
    def update_model(self, json=None, **kw):
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
        return self.s.post(path, json=json)
    
    def train(self, model_id:int,):
        path = f'app/user/model/train/{model_id}'
        return self.s.post(path)

    def theme_list(self):
        path = f'/app/theme/list'
        return self.s.get(path)
    
    def theme_detail(self, theme_id):
        path = f'/app/theme/detail/{theme_id}'
        return self.s.get(path)
    
    def output_po(self, json=None, **kw):
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
        return self.s.post(path, json=json)

    def template_list(self):
        path = '/app/template/list'
        return self.s.get(path)

    def subscribe(self):
        '''need to call wx api
        json: {
            "key": "9ce51182-eb1a-479d-8a13-b00fc01c2e65",
            "location": "image",
            "templateId": "UG_tzP8x-STvlGEZCIXVxI_ZBLYendyZXgCLCm6wpkM"
        }'''
        path = '/app/template/subscribe'

def upload(file, url, data):
    s = Session()
    with open(file, 'rb') as f:
        s.post(url, data=data, files={data['key']:f})