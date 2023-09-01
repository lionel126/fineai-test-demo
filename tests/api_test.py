import os
import time
import pytest
from api.app import App, upload

not_face_file = '/Users/chensg/Downloads/891.jpg'
# face = '/Users/chensg/Pictures/scarlettJohansson/R (3).jpeg'
scarlett_face = '/Users/chensg/Pictures/scarlettJohansson/R.jpeg'
scarlett_dir = '/Users/chensg/Pictures/scarlettJohansson'
# daddario_dir = '/Users/chensg/Pictures/Alexandra Daddario'
# captain_dir = '/Users/chensg/Pictures/americanCaptain'

face_file = scarlett_face
file_dir = scarlett_dir
files = [os.path.join(file_dir, f) for f in os.listdir(file_dir)]

@pytest.mark.parametrize('user, face, dataset', [
    ('c', face_file, files),
])
def test_train(user, face, dataset):

    app = App(user)

    model_id = app.create_model().json()['data']['id']

    # 正脸
    json = {"modelId": model_id, "fileName": face}
    data = app.create_face(json).json()['data']
    image_id = data['id']
    upload(face, data['host'], data['uploadParam'])

    job_id = app.finish_face({"imageId": image_id, "modelId": model_id}).json()[
        'data']['jobId']

    # # 补充
    # fs = app.create_dataset(model_id, dataset).json()['data']
    # ids = []
    # for f in fs:
    #     upload(f['fileName'], f['host'], f['uploadParam'])
    #     ids.append(f['id'])
    # job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
    # print(f'dataset job: {job_id}')
    # app.update_model(id=model_id, modelName=f'{model_id}-Scarlett')
    # while app.job_state(job_id).json()['data']['status'] != 'success':
    #     time.sleep(1)
    
    # app.train(model_id)


@pytest.mark.parametrize('job_id', [
    '062be8eb-65b5-47e0-b4fb-c908169302df'
])
def test_job_state(job_id):

    app = App('c')
    j = app.job_state(job_id).json()
    print(f'{job_id}: {j}')

@pytest.mark.parametrize('model_id, ids', [
    (307, [1693, 1692, 5503, 5501, 5487, 5413, 5405, 5360, 5346, 5341, 5221, 5458, 5476, 5465, 5453, 5447, 5444, 5424, 5425, 5426, 5427, 5428, 5429, 5430, 5431, 5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, 5440, 5441, 5442, 5443, 5445, 5446, 5448, 5327, 5328, 5449, 5450, 5451, 5452, 5454, 5457, 5455, 5456, 5459, 5460 ]),
    # (83, [1693, 1692])
])
def test_finish_dataset(model_id, ids):
    app =App()
    app.finish_dataset(model_id, ids)


@pytest.mark.parametrize('user, model_id, image_id', [
    # ('b', 83, 1693), 
    # ('', 83, 1692),
    # ('c', 336, 6365), # illegal model 
    # ('c', 336, 5555), # 333, 5555
    # ('c', 336, 5524) # 333, 5545
    # ('c', 336, 6363),
    ('b', 333, 6192)
])
def test_finish_face_with_old_image_id(user, model_id, image_id):
    
    app =App(user)
    json = {
        "modelId": model_id,
        "imageId": image_id
    }
    job_id = app.finish_face(json).json()['data']['jobId']
    
    while True:
        data = app.job_state(job_id).json()['data']
        if data['status'] != 'success':
            time.sleep(1)
            continue
        break
    print(data['faceDetectionResult']['status'], data['faceDetectionResult']['reason'])


@pytest.mark.parametrize('user, model_id, face_file', [
    # ('c', 333, face_file),
    ('b', 333, face_file),
])
def test_finish_face_with_new_image(user, model_id, face_file):
    # create face
    app = App(user)
    json = {"modelId": model_id, "fileName": face_file}
    data = app.create_face(json).json()['data']
    
    # finish face
    image_id = data['id']
    upload(face_file, data['host'], data['uploadParam'])

    job_id = app.finish_face({"imageId": image_id, "modelId": model_id}).json()[
        'data']['jobId']
    
    while True:
        data = app.job_state(job_id).json()['data']
        if data['status'] != 'success':
            time.sleep(1)
            continue
        break
    print(data['faceDetectionResult']['status'], data['faceDetectionResult']['reason'])


@pytest.mark.parametrize('user, model_id, ids', [
    # ('c', 333, face_file),
    # ('c', 360, [ 6474, 6475, 6476, 6477, 6478, 6479, 6480, 6481, 6482, 6483, 6484, 6485, 6486, 6487, 6488, 6489, 6490, 6491, 6492, 6493, 6494, 6495, 6496, 6497, 6498, 6499, 6500, 6501, 6502, 6503, 6504, 6505, 6506, 6507, 6508, 6509, 6510, 6511, 6512, 6513, 6514, 6515, 6516, 6517, 6518, 6519 ]),
    ('c', 360, [6164, 6165, 6166, 6167, 6168, 6169, 6170, 6171, 6172, 6173, 6174, 6175, 6176, 6177, 6178, 6179, 6180, 6181, 6182, 6183, 6184, 6185, 6186, 6187, 6188, 6189, 6190, 6191]),
])
def test_finish_dataset_with_old_image(user, model_id, ids):
    # create dataset
    app = App(user)
    
    # fs = app.create_dataset(model_id, dataset).json()['data']
    # ids = []
    # for f in fs:
    #     upload(f['fileName'], f['host'], f['uploadParam'])
    #     ids.append(f['id'])
    job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
    while True:
        data = app.job_state(job_id).json()['data']
        if data['status'] == 'success':
            break
        time.sleep(1)
    print(data['datasetVerifyResult']['status'], data['faceDetectionResult']['reason'])

@pytest.mark.parametrize('user, model_id, dataset', [
    # ('c', 333, face_file),
    ('b', 333, files[:1]),
])
def test_finish_dataset_with_new_image(user, model_id, dataset):
    # create dataset
    app = App(user)
    
    fs = app.create_dataset(model_id, dataset).json()['data']
    ids = []
    for f in fs:
        upload(f['fileName'], f['host'], f['uploadParam'])
        ids.append(f['id'])
    job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
    while True:
        data = app.job_state(job_id).json()['data']
        if data['status'] == 'success':
            break
        time.sleep(1)
    print(data['datasetVerifyResult']['status'], data['faceDetectionResult']['reason'])