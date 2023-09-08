import time
from random import sample
from locust import HttpUser, task, between
from api.config import settings

cert = settings.REQUESTS_CA_BUNDLE
proxies = {'http': settings.http_proxy, 'https': settings.https_proxy}
delay = 3

checked = [15600, 15604, 15605, 15607, 15578, 15580, 15581, 15583, 15584, 15585, 15588, 15589, 15590, 15591, 15593, 15586, 15621, 15623, 15624, 15594, 15597, 15598, 15609, 15610, 15617, 15608, 15611, 15615, 15625, 15626, 15627, 15628, 15629]
invalid = [15599, 15601, 15602, 15603, 15606, 15579, 15582, 15587, 15592, 15596, 15620, 15622, 15618, 15613, 15614, 15616, 15619]
class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    host = settings.app_base_url
    
    def on_start(self):
        # self.client.post("/login", json={"username":"foo", "password":"bar"})
        self.client.cookies.update({settings.token_key: settings.token})

    @task
    def train(self):
        job_id = self.client.post(
            "/app/user/model/image/face/finish", 
            json={
                "imageId": 16705,
                "modelId": 555
            }).json()['data']['jobId']
        while self.client.get(f'/app/user/model/job/state/{job_id}').json()['data']['status'] in ('create', 'pending'):
            # ('success', 'fail')
            time.sleep(delay)
            continue

        self.client.post("/app/user/model/image/dataset/finish?modelId=555", json=sample(checked, k=25)+sample(invalid, k=5))

        while self.client.get(f'/app/user/model/job/state/{job_id}').json()['data']['status'] in ('create', 'pending'):
            # ('success', 'fail')
            time.sleep(delay)
            continue

    @task(1)
    def output(self):
        json={
            "modelId": 556,
            "themeId": 6,
            "themeModelId": 1
        }
        
        job_id = self.client.post("/app/image/output/portray", json=json).json()['data']['jobId']
        while self.client.get(f"/app/image/output/detail/{job_id}").json()['data']['status'] in ('create', 'pending'):
            # ('success', 'fail')
            time.sleep(delay)
            continue
            