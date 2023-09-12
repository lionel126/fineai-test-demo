import logging
from sqlalchemy import select, update
import time
import gevent
from requests.cookies import cookiejar_from_dict
from locust import task, between, TaskSet
from locust.contrib.fasthttp import FastHttpUser, FastResponse
from locust_plugins.csvreader import CSVReader
from api.config import settings
from fineai_test.db.app import UploadImageFile
from fineai_test.db import Sess as Asess
from api.db import Sess

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# log_sql = logging.getLogger('sqlalchemy')
# log_sql.setLevel(logging.DEBUG)

csv_data = CSVReader(".data")

def resurge(image_id):
    with Sess() as s:
        stmt = update(UploadImageFile).where(UploadImageFile.id == image_id).values(is_delete=False)
        ret = s.execute(stmt)
        s.commit()

class UserBehavior(TaskSet):

    def on_start(self):
        cookie_jar = cookiejar_from_dict({settings.token_key: settings.token})
        self.client.client.cookiejar = cookie_jar
        data = next(csv_data)
        self.model_id, self.face_id, self.image_ids = int(data[0]), int(data[1]), list(map(int, data[2:]))
        self.dataset_job_id = '3648ad22-8a80-4854-8236-3bb00e07f32d'

    @task
    def train(self):
        start = time.time()        
        face_job_id = self.client.post(
            "/app/user/model/image/face/finish",
            json={
                "imageId": self.face_id,
                "modelId": self.model_id
            }).json()['data']['jobId']
        
        count = 0
        while True:
            gevent.sleep(1)
            res = self.client.get(f'/app/user/model/job/state/{face_job_id}')
            if res.json()['data']['status'] == 'success':
                break
            
            count += 1
            if settings.loop_count and count > settings.loop_count:
                break
        log.debug(f'model={self.model_id},face detection job count: {count}')
        
        # resurge(self.face_id)
        
        jsn = self.client.post(f"/app/user/model/image/dataset/finish?modelId={self.model_id}", json=self.image_ids).json()
        log.debug(f'model={self.model_id},dataset: {jsn}')
        dataset_job_id = jsn['data']['jobId']
        self.dataset_job_id = dataset_job_id

        count = 0
        while True:
            gevent.sleep(1)
            res = self.client.get(f'/app/user/model/job/state/{dataset_job_id}')
            if res.json()['data']['status'] == 'success':
                break
            count += 1
            if settings.loop_count and count > settings.loop_count:
                break
        log.debug(f'model={self.model_id},dataset job count: {count}')

        res = self.client.post(f"/app/user/model/train/{self.model_id}")
        end = time.time()
        log.debug(f'model={self.model_id},duration:{end-start},train: {res.status_code}, {res.text}')
    
    @task(10)
    def job_state(self):
        log.debug(f'{self.dataset_job_id=}')
        self.client.get(f'/app/user/model/job/state/{self.dataset_job_id}')

    @task(5)
    def portray(self):
        jsn = {
            "modelId": 100,
            "themeId": 3,
            "themeModelId": 1
        }
        res = self.client.post(f'/app/image/output/portray', json=jsn)        
        log.debug(f'model={self.model_id}, portray:{res.json()}')
        job_id = res.json()['data']['jobId']
        
        count = 0
        while self.client.get(f'/app/image/output/detail/{job_id}').json()['data']['status'] != 'success':
            gevent.sleep(1)
            count += 1
            if count > 10:
                break

class MyLocust(FastHttpUser):
    # wait_time = between(1, 2)
    host = settings.app_base_url
    tasks = [UserBehavior]