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
            # if count > 50:
            #     break
        log.debug(f'model={self.model_id},face detection job count: {count}')
        
        resurge(self.face_id)
        
        jsn = self.client.post(f"/app/user/model/image/dataset/finish?modelId={self.model_id}", json=self.image_ids).json()
        log.debug(f'model={self.model_id},dataset: {jsn}')
        dataset_job_id = jsn['data']['jobId']

        count = 0
        while True:
            
            gevent.sleep(1)
            res = self.client.get(f'/app/user/model/job/state/{dataset_job_id}')
            if res.json()['data']['status'] == 'success':
                break
            count += 1
            # if count > 50:
            #     break
        log.debug(f'model={self.model_id},dataset job count: {count}')

        res = self.client.post(f"/app/user/model/train/{self.model_id}")
        end = time.time()
        log.debug(f'model={self.model_id},duration:{end-start},train: {res.status_code}, {res.text}')
        

class MyLocust(FastHttpUser):
    wait_time = between(1, 2)
    host = settings.app_base_url
    tasks = [UserBehavior]