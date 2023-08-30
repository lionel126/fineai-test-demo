import os
import pytest
from api.app import App, upload



def test_dataset_create():
    file = '/Users/chensg/Pictures/6094e19d8f146.jpeg'

    model_id = 78
    # image_id = 1384
    # ids = list(range(1399, 1413))
    # job_id = '401c1750-b46e-45a4-9c72-aa042df25c7c'

    app = App()

    # model_id = app.create_model().json()['data']['id']

    json = {"modelId": model_id, "fileName": file.split('/')[-1]}
    data = app.create_face(json).json()['data']
    image_id = data['id']
    upload(file, data['host'], data['uploadParam'])

    job_id = app.finish_face({"imageId": image_id, "modelId": model_id}).json()[
        'data']['jobId']

    # dataset = os.listdir(dataset_dir)
    # fs = app.create_dataset(model_id, dataset).json()['data']
    # ids = []
    # for f in fs:
    #     upload(os.path.join(dataset_dir, f['fileName']), f['host'], f['uploadParam'])
    #     ids.append(f['id'])
    # job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
    # print(f'dataset job: {job_id}')


@pytest.mark.parametrize('job_id', [
    '8a040fa4-d865-433f-8e95-d2e9e4a5adbe'
])
def test_job_state(job_id):

    app = App()
    j = app.job_state(job_id).json()
    print(f'{job_id}: {j}')
