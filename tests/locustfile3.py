import logging
from requests.cookies import cookiejar_from_dict
from locust import task, TaskSet
from locust.contrib.fasthttp import FastHttpUser
from api.config import settings


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# log_sql = logging.getLogger('sqlalchemy')
# log_sql.setLevel(logging.DEBUG)

class UserBehavior(TaskSet):

    def on_start(self):
        cookie_jar = cookiejar_from_dict({settings.token_key: settings.token})
        self.client.client.cookiejar = cookie_jar

    
    @task
    def job_state(self):
        
        res = self.client.get('/app/user/model/job/state/ad62652f-bff4-4aa3-a096-da014b24db4c')
        log.debug(f'job state : {res.text}')

        
    @task
    def output_detail(self):
        res = self.client.get('/app/image/output/detail/bb47911c-1e07-45b1-94cd-cc26ea18e33d')
        log.debug(f'output detail: {res.text}')
        
class MyLocust(FastHttpUser):
    # wait_time = between(1, 2)
    host = settings.app_base_url
    tasks = [UserBehavior]