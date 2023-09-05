import random
import os
import time
import pytest
from api.app import App, upload

scarlett_dir = '/Users/chensg/Pictures/scarlettJohansson'
daddario_dir = '/Users/chensg/Pictures/Alexandra Daddario'
captain_dir = '/Users/chensg/Pictures/americanCaptain'

face_ext_heif = '/Users/chensg/Pictures/scarlettJohansson/379.heif'
face_ext_avif = '/Users/chensg/Pictures/hero.avif' # not supported file format
face_not_human = '/Users/chensg/Downloads/891.jpg'
face_too_many = '/Users/chensg/Pictures/scarlettJohansson/marvel-scarlett-johansson-zoe-saldana-dave-bautista-done-with-mcu.jpg'
face_scarlett2 = '/Users/chensg/Pictures/scarlettJohansson/R (4).jpeg'
face_scarlett = '/Users/chensg/Pictures/scarlettJohansson/R.jpeg'
face_daddario_random = os.path.join(daddario_dir, os.listdir(daddario_dir)[random.randint(0, len(os.listdir(daddario_dir))-1)])

error_files = [face_ext_avif, face_not_human, face_too_many]
images_scarlett = [os.path.join(scarlett_dir, f) for f in os.listdir(scarlett_dir)]
images_daddario = [os.path.join(daddario_dir, f) for f in os.listdir(daddario_dir)]


@pytest.mark.parametrize('user, model_id, face, dataset, update, train', [
    # ('c', None, face_file, files, False, False),
    # ('b', 342, None, None, None, True),
    # ('c', None, face_scarlett, images_scarlett, None, True),
    # ('c', None, face_daddario_random, images_daddario, None, True),
    # ('c', None, face_daddario_random, images_daddario, {'gender': 'male'}, True),
    # ('c', None, face_daddario_random, images_daddario, None, False),
    ('b', None, face_scarlett2, None, None, False),
])
def test_train(user:str|None, model_id:int|None, face:str|None, dataset:list[str]|None, update:dict|None, train:bool):

    app = App(user)

    if not model_id:
        model_id = app.create_model().json()['data']['id']

    # 正脸
    if face:
        json = {"modelId": model_id, "fileName": face}
        data = app.create_face(json).json()['data']
        image_id = data['id']
        upload(face, data['host'], data['uploadParam'])

        job_id = app.finish_face({"imageId": image_id, "modelId": model_id}).json()[
            'data']['jobId']
        
        while data:=app.job_state(job_id).json()['data']:
            if data['status'] != 'success':
                time.sleep(1)
                continue
            # if data['faceDetectionResult']['status'] != 'checked':
            #     return
            if data['faceDetectionResult']['status'] == 'checked':
                break

    # 补充
    # if dataset:
    # face合格后上传
    if dataset and data['faceDetectionResult']['status'] == 'checked':
        fs = app.create_dataset(model_id, dataset).json()['data']
        ids = []
        for f in fs:
            upload(f['fileName'], f['host'], f['uploadParam'])
            ids.append(f['id'])
        job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
        print(f'dataset job: {job_id}')        
        while app.job_state(job_id).json()['data']['status'] != 'success':
            time.sleep(1)
    
    model_name = f'{model_id}-{update.pop("modelName")}' if (update and 'modelName' in update) else f'{model_id}-'
    app.update_model(id=model_id, modelName=model_name, **update if update else {})

    if train:
        app.train(model_id)


@pytest.mark.parametrize('job_id', [
    '062be8eb-65b5-47e0-b4fb-c908169302df'
])
def test_job_state(job_id):

    app = App('c')
    j = app.job_state(job_id).json()
    print(f'{job_id}: {j}')


@pytest.mark.parametrize('user, model_id, image_id', [
    # ('b', 83, 1693), 
    # ('', 83, 1692),
    # ('c', 336, 6365), # illegal model 
    # ('c', 336, 5555), # 333, 5555
    # ('c', 336, 5524) # 333, 5545
    # ('c', 336, 6363),
    # ('b', 333, 6192),
    # ('b', 387, 7111), # finish 他人model+face
    ('b', 387, 7118), # 别人model+自己的图
    # ('b', 330, 6600), # 文件不支持avif
    # ('b', 330, 6601), # 文件不存在
    # ('b', 330, 6610), # 没脸
    # ('b', 300, 6611), # 多脸
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
    print(data['status'])


@pytest.mark.parametrize('user, model_id, face_file', [
    # ('c', 333, face_file),
    # ('b', 333, face_file),
    # ('b', 330, face_file2),
    ('b', 331, face_daddario_random)
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
    # ('c', 360, [6164, 6165, 6166, 6167, 6168, 6169, 6170, 6171, 6172, 6173, 6174, 6175, 6176, 6177, 6178, 6179, 6180, 6181, 6182, 6183, 6184, 6185, 6186, 6187, 6188, 6189, 6190, 6191]),
    # ('b', 330, [6600, 6601, 6610, 6611]), # 文件不支持avif, 文件不存在, 没脸, 多脸
    # ('b', 330, [ 6786, 6787, 6788, 6789, 6790, 6791, 6792, 6793, 6794, 6795, 6796, 6797, 6798, 6799, 6800, 6801, 6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809, 6810, 6811, 6812, 6813, 6814, 6815, 6816, 6817, 6818, 6819, 6820, 6821, 6822, 6823, 6824, 6825, 6826, 6827, 6828, 6829, 6830, 6831, 6832, 6833, 6834 ]),
    ('c', 330, [ 6786, 6787, 6788, 6789, 6790, 6791, 6792, 6793, 6794, 6795, 6796, 6797, 6798, 6799, 6800, 6801, 6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809, 6810, 6811, 6812, 6813, 6814, 6815, 6816, 6817, 6818, 6819, 6820, 6821, 6822, 6823, 6824, 6825, 6826, 6827, 6828, 6829, 6830, 6831, 6832, 6833, 6834 ]),
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
    print([{'id': d['id'], 'reason': d['reason']} for d in data['datasetVerifyResult']])

@pytest.mark.parametrize('user, model_id, dataset', [
    # ('c', 333, face_file),
    # ('b', 333, files[:1]),
    # ('b', 330, [image_avif, image_heif, image_no_face, image_too_many_faces]),
    # ('b', 330, files + error_files),
    ('b', 342, images_scarlett[0:1]),

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
    print([{'id': d['id'], 'reason': d['reason']} for d in data['datasetVerifyResult']])
