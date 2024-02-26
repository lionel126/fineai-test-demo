import logging
from requests.cookies import cookiejar_from_dict
from locust import task, TaskSet
from locust.contrib.fasthttp import FastHttpUser

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# log_sql = logging.getLogger('sqlalchemy')
# log_sql.setLevel(logging.DEBUG)

class UserBehavior(TaskSet):

    def on_start(self):
        # user_id = 22
        # iss = 'https://xw.fineai.pro' , inside pod
        cookie_jar = cookiejar_from_dict({'USER-COOKIE-TOKEN-PROD': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlvbklkIjoiVzRBdm9RbXlSWGRreWFKNSIsInN1YiI6IlhXIElUIENvLiIsImlzcyI6Imh0dHBzOi8veHcuZmluZWFpLnBybyIsImxvZ2luX3VzZXJfa2V5IjoiZDZhZmFjNjhmODllYmQ3ZGZmY2E0NmJmNDdjNzI3ZDMifQ.Wnal5mg9nRyVFhEW5JhSddy7sNlnQXHlI1VPU6uGv6U'})
        self.client.client.cookiejar = cookie_jar

    
    # @task
    # def job_state(self):
        
    #     res = self.client.get('/app/user/model/job/state/ad62652f-bff4-4aa3-a096-da014b24db4c')
    #     log.debug(f'job state : {res.text}')

    # @task
    # def output_detail(self):
    #     res = self.client.get('/app/image/output/detail/bb47911c-1e07-45b1-94cd-cc26ea18e33d')
    #     log.debug(f'output detail: {res.text}')

    @task
    def output_detail_0(self):
        self.client.get('/app/image/output/detail/39a1af6c-7581-4c80-9b85-91e085afecd4')
        # log.debug(f'output detail: {res.text}')
    @task
    def output_detail_1(self):
        self.client.get('/app/image/output/detail/cc0b5d7b-10cf-4853-8361-d186d4708e58')
    
    @task
    def output_detail_2(self):
        self.client.get('/app/image/output/detail/2df38032-c07c-4593-8a1c-3b415b016035')
    

class MyLocust(FastHttpUser):
    # wait_time = between(1, 2)
    host = 'https://xw.fineai.pro'
    tasks = [UserBehavior]