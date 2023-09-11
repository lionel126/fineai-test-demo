import gevent
from requests.cookies import cookiejar_from_dict
from locust import task, between, TaskSet
from locust.contrib.fasthttp import FastHttpUser
from locust_plugins.csvreader import CSVReader
from api.config import settings

csv_data = CSVReader(".data")


# class UserBehavior(TaskSet):

#     def on_start(self):
#         self.client.cookies.update({settings.token_key: settings.token})
#         data = next(csv_data)
#         self.model_id, self.face_id, self.image_ids = int(data[0]), int(data[1]), list(map(int, data[2].split(',')))

#     @task
#     def train(self):
        
        
#         # job_id = self.client.post(
#         #     "/app/user/model/image/face/finish",
#         #     json={
#         #         "imageId": self.face_id,
#         #         "modelId": self.model_id
#         #     }).json()['data']['jobId']
#         res = self.client.post(
#             "/app/user/model/image/face/finish",
#             json={
#                 "imageId": self.face_id,
#                 "modelId": self.model_id
#             })
#         print(res.json())
#         job_id = res.json()['data']['jobId']
#         count = 10
#         while count > 0:
#             self.client.get(f'/app/user/model/job/state/{job_id}')
#             count -= 1

#         self.client.post(f"/app/user/model/image/dataset/finish?modelId={self.model_id}", json=self.image_ids)

#         count = 10
#         while count > 0:
#             self.client.get(f'/app/user/model/job/state/{job_id}')
#             count -= 1

# class MyLocust(HttpUser):
#     host = settings.app_base_url
#     tasks = [UserBehavior]




class UserBehavior(TaskSet):

    def on_start(self):
        cookie_jar = cookiejar_from_dict({settings.token_key: settings.token})
        self.client.client.cookiejar = cookie_jar
        data = next(csv_data)
        self.model_id, self.face_id, self.image_ids = int(data[0]), int(data[1]), list(map(int, data[2:]))

    @task
    def train(self):        
        face_job_id = self.client.post(
            "/app/user/model/image/face/finish",
            json={
                "imageId": self.face_id,
                "modelId": self.model_id
            }).json()['data']['jobId']
        
        count = 10
        while count > 0:
            gevent.sleep(1)
            self.client.get(f'/app/user/model/job/state/{face_job_id}')
            count -= 1

        # dataset_job_id = self.client.post(f"/app/user/model/image/dataset/finish?modelId={self.model_id}", json=self.image_ids).json()['data']['jobId']
        jsn = self.client.post(f"/app/user/model/image/dataset/finish?modelId={self.model_id}", json=self.image_ids).json()
        print(jsn)
        dataset_job_id = jsn['data']['jobId']

        count = 10
        while count > 0:
            gevent.sleep(1)
            self.client.get(f'/app/user/model/job/state/{dataset_job_id}')
            count -= 1

        res = self.client.post(f"/app/user/model/train/{self.model_id}")
        print(res, res.text)

class MyLocust(FastHttpUser):
    wait_time = between(1, 2)
    host = settings.app_base_url
    tasks = [UserBehavior]