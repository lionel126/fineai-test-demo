from .session import Session
from .config import settings


class Internal():
    def __init__(self):
        self.s = Session(settings.internal_base_url)

    def train(self, modelId):
        self.s.post(f'model/train/{modelId}')

    def generate_avatar(self, modelId):
        self.s.post(f'model/output/avatar/{modelId}')
