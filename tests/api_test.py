import os
import time
import pytest
from api.app import App, upload

face = '/Users/chensg/Pictures/scarlettJohansson/R.jpeg'
# face = '/Users/chensg/Pictures/scarlettJohansson/R (3).jpeg'
file_dir = '/Users/chensg/Pictures/scarlettJohansson'

# file_dir = '/Users/chensg/Pictures/Alexandra Daddario'
# file_dir = '/Users/chensg/Pictures/americanCaptain'
files = [os.path.join(file_dir, f) for f in os.listdir(file_dir)]

@pytest.mark.parametrize('user, face, dataset', [
    ('b', files[14], files),
])
def test_train(user, face, dataset):

    app = App(user)

    model_id = app.create_model().json()['data']['id']

    json = {"modelId": model_id, "fileName": face.split('/')[-1]}
    data = app.create_face(json).json()['data']
    image_id = data['id']
    upload(face, data['host'], data['uploadParam'])

    job_id = app.finish_face({"imageId": image_id, "modelId": model_id}).json()[
        'data']['jobId']

    fs = app.create_dataset(model_id, dataset).json()['data']
    ids = []
    for f in fs:
        upload(f['fileName'], f['host'], f['uploadParam'])
        ids.append(f['id'])
    job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
    print(f'dataset job: {job_id}')
    app.update_model(id=model_id, modelName=f'{model_id}-Scarlett')
    while app.job_state(job_id).json()['data']['status'] != 'success':
        time.sleep(1)
    app.train(model_id)


@pytest.mark.parametrize('job_id', [
    '8a040fa4-d865-433f-8e95-d2e9e4a5adbe'
])
def test_job_state(job_id):

    app = App()
    j = app.job_state(job_id).json()
    print(f'{job_id}: {j}')

@pytest.mark.parametrize('model_id, ids', [
    (307, [1693, 1692, 5503, 5501, 5487, 5413, 5405, 5360, 5346, 5341, 5221, 5458, 5476, 5465, 5453, 5447, 5444, 5424, 5425, 5426, 5427, 5428, 5429, 5430, 5431, 5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, 5440, 5441, 5442, 5443, 5445, 5446, 5448, 5327, 5328, 5449, 5450, 5451, 5452, 5454, 5457, 5455, 5456, 5459, 5460 ]),
    # (83, [1693, 1692])
])
def test_finish_dataset(model_id, ids):
    app =App()
    app.finish_dataset(model_id, ids)


@pytest.mark.parametrize('model_id, image_id', [
    (83, 1693), 
    # (83, 1692)
])
def test_finish_face(model_id, image_id):
    app =App()
    json = {
        "modelId": model_id,
        "imageId": image_id
    }
    app.finish_face(json)
