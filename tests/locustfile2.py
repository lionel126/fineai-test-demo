import logging
from sqlalchemy import select, update
import time
import gevent
from requests.cookies import cookiejar_from_dict
from locust import task, between, TaskSet
from locust.contrib.fasthttp import FastHttpUser, FastResponse
from locust_plugins.csvreader import CSVReader
from api.config import settings
from fineai_test.db.app import UploadImageFile, UserModel
from fineai_test.db import Sess as Asess
from api.db import Sess

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# log_sql = logging.getLogger('sqlalchemy')
# log_sql.setLevel(logging.DEBUG)

csv_data = CSVReader(".data")

def resurge(model_id):
    with Sess() as s:
        stmt = update(UserModel).where(UserModel.id == model_id).values(status='pending')
        ret = s.execute(stmt)
        s.commit()

class UserBehavior(TaskSet):

    def on_start(self):
        cookie_jar = cookiejar_from_dict({settings.token_key: settings.token})
        self.client.client.cookiejar = cookie_jar
        self.model_id = int(next(csv_data)[0])

    @task(3)
    def face(self):
        res = self.client.post(
            "/app/user/model/image/face/finish",
            json={
                "imageId": 43169,
                "modelId": 1372
            })
        
        log.debug(f'face: model=1372,{res.json()}')

    @task(3)
    def dataset(self):

        res = self.client.post(f"/app/user/model/image/dataset/finish?modelId=1345", json=[42627,42658,42631,42673,42639,42630,42637,42662,42656,42667,42670,42663,42644,42672,42651,42634,42675,42654,42646,42674,42650,42671,42636,42657,42629,42632,42645,42648,42624,42647])
        log.debug(f'dataset: model=1345,{res.json()}')
        

    @task
    def train(self):
        model_id = self.model_id
        resurge(model_id)   
        res = self.client.post(f"/app/user/model/train/{model_id}")        
        log.debug(f'train: model={model_id},{res.text}')
    
    @task(10)
    def job_state(self):
        
        res = self.client.get(f'/app/user/model/job/state/3648ad22-8a80-4854-8236-3bb00e07f32d')
        log.debug(f'job state : {res.json()}')

    @task(5)
    def portray(self):
        jsn = {
            "modelId": 100,
            "themeId": 3,
            "themeModelId": 1
        }
        res = self.client.post(f'/app/image/output/portray', json=jsn)        
        log.debug(f'portray: model 100, {res.json()}')
        
    @task(10)
    def output_detail(self):
        res = self.client.get(f'/app/image/output/detail/cc6a0806-1796-4931-8bcd-170f220eff74')
        log.debug(f'output detail: {res.json()}')
        
class MyLocust(FastHttpUser):
    # wait_time = between(1, 2)
    host = settings.app_base_url
    tasks = [UserBehavior]