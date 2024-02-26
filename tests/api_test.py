from random import choice, sample
import time
import pytest
from api.app import App, upload
from api import db
from api.config import settings
from api.utils import files

scarlett = settings.scarlett
daddario = settings.daddario
captain = settings.captain
guoda = settings.guoda
jason = settings.jason
lf = settings.lf

face_ext_heif = '/Users/chensg/Pictures/scarlettJohansson/379.heif'
face_ext_avif = '/Users/chensg/Pictures/hero.avif'  # not supported file format
face_not_human = '/Users/chensg/Downloads/891.jpg'
face_too_many = '/Users/chensg/Pictures/scarlettJohansson/marvel-scarlett-johansson-zoe-saldana-dave-bautista-done-with-mcu.jpg'
face_scarlett2 = '/Users/chensg/Pictures/scarlettJohansson/R (4).jpeg'
face_scarlett = '/Users/chensg/Pictures/scarlettJohansson/R.jpeg'

error_files = [face_ext_avif, face_not_human, face_too_many]


@pytest.mark.parametrize('uid, model_id, face, dataset, update, train', [
    # ('c', None, choice(pics(scarlett)), pics(scarlett), {'modelName': 'scar'}, True),
    # ('c', None, choice(pics(daddario)), pics(daddario), {'modelName': 'daddario'}, True),

    # ('c', 491, choice(pics(daddario)), pics(
    #     daddario), {'modelName': 'daddario'}, True),

    ('c', 494, choice(files(daddario)), files(
        daddario), {'modelName': 'daddario'}, True),

])
def test_train(uid: str | int | None, model_id: int | None, face: str | int | None, dataset: list[str] | list[int] | None, update: dict | None, train: bool):
    '''face, dataset: local file if type is str; image id if type is int. support str & int mixed in dataset
    '''

    app = App(uid)

    # include previous images or not
    include_previous_images = False
    if model_id:
        include_previous_images = True

    if not model_id:
        model_id = app.create_model().json()['data']['id']

    model_name = f'{model_id}-{update.pop("modelName")}' if (
        update and 'modelName' in update) else f'{model_id}-'
    app.update_model(id=model_id, modelName=model_name,
                     **update if update else {})

    # 正脸
    if face:
        if isinstance(face, str):
            json = {"modelId": model_id, "fileName": face}
            data = app.create_face(json).json()['data']
            upload(face, data['host'], data['uploadParam'])
            image_id = data['id']
        else:
            # isinstance(face, int)
            image_id = face

        job_id = app.finish_face({"imageId": image_id, "modelId": model_id}).json()[
            'data']['jobId']

        while data := app.job_state(job_id).json()['data']:
            if data['status'] != 'success':
                time.sleep(2)
                continue
            # if data['faceDetectionResult']['status'] != 'checked':
            #     return
            if data['faceDetectionResult']['status'] == 'checked':
                break
            else:
                return

    # 补充
    # if dataset:
    # face合格后上传
    if dataset:
        ids = [image.id for image in db.get_dataset_images(
            model_id) if image.status == 'invalid'] if include_previous_images else []
        if len(ids) < 200:
            images = []
            for file in dataset:
                if isinstance(file, int):
                    ids.append(file)
                else:
                    # isinstance(file, str)
                    images.append(file)
            if images:
                fs = app.create_dataset(model_id, images).json()['data']
                for f in fs:
                    upload(f['fileName'], f['host'], f['uploadParam'])
                    ids.append(f['id'])
        if len(ids) > 200:
            ids = sample(ids, k=200)
        job_id = app.finish_dataset(model_id, ids).json()['data']['jobId']
        while app.job_state(job_id).json()['data']['status'] != 'success':
            time.sleep(1)

    if train:
        app.train(model_id)


@pytest.mark.parametrize('user, model_id', [
    ('c', 413),
])
def test_output(user, model_id):
    app = App(user)
    theme_id = choice(app.theme_list().json()['data'])['id']
    theme_model_id = choice(app.theme_detail(
        theme_id).json()['data']['modelList'])['id']
    app.output_portray(modelId=model_id, themeId=theme_id,
                       themeModelId=theme_model_id)


@pytest.mark.parametrize('job_id', [
    '062be8eb-65b5-47e0-b4fb-c908169302df'
])
def test_job_state(job_id):

    app = App('c')
    app.job_state(job_id).json()


@pytest.mark.parametrize('user, model_id, image_id', [
    # ('b', 83, 1693),
    # ('', 83, 1692),
    # ('c', 336, 6365), # illegal model
    # ('c', 336, 5555), # 333, 5555
    # ('c', 336, 5524) # 333, 5545
    # ('c', 336, 6363),
    # ('b', 333, 6192),
    # ('b', 387, 7111), # finish 他人model+face
    ('b', 387, 7118),  # 别人model+自己的图
    # ('b', 330, 6600), # 文件不支持avif
    # ('b', 330, 6601), # 文件不存在
    # ('b', 330, 6610), # 没脸
    # ('b', 300, 6611), # 多脸
])
def test_finish_face_with_old_image_id(user, model_id, image_id):

    app = App(user)
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
    ('b', 331, choice(files(daddario)))
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
    print(data['faceDetectionResult']['status'],
          data['faceDetectionResult']['reason'])


@pytest.mark.parametrize('user, model_id, ids', [
    # ('c', 333, face_file),
    # ('c', 360, [ 6474, 6475, 6476, 6477, 6478, 6479, 6480, 6481, 6482, 6483, 6484, 6485, 6486, 6487, 6488, 6489, 6490, 6491, 6492, 6493, 6494, 6495, 6496, 6497, 6498, 6499, 6500, 6501, 6502, 6503, 6504, 6505, 6506, 6507, 6508, 6509, 6510, 6511, 6512, 6513, 6514, 6515, 6516, 6517, 6518, 6519 ]),
    # ('c', 360, [6164, 6165, 6166, 6167, 6168, 6169, 6170, 6171, 6172, 6173, 6174, 6175, 6176, 6177, 6178, 6179, 6180, 6181, 6182, 6183, 6184, 6185, 6186, 6187, 6188, 6189, 6190, 6191]),
    # ('b', 330, [6600, 6601, 6610, 6611]), # 文件不支持avif, 文件不存在, 没脸, 多脸
    # ('b', 330, [ 6786, 6787, 6788, 6789, 6790, 6791, 6792, 6793, 6794, 6795, 6796, 6797, 6798, 6799, 6800, 6801, 6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809, 6810, 6811, 6812, 6813, 6814, 6815, 6816, 6817, 6818, 6819, 6820, 6821, 6822, 6823, 6824, 6825, 6826, 6827, 6828, 6829, 6830, 6831, 6832, 6833, 6834 ]),
    ('c', 330, [6786, 6787, 6788, 6789, 6790, 6791, 6792, 6793, 6794, 6795, 6796, 6797, 6798, 6799, 6800, 6801, 6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809,
     6810, 6811, 6812, 6813, 6814, 6815, 6816, 6817, 6818, 6819, 6820, 6821, 6822, 6823, 6824, 6825, 6826, 6827, 6828, 6829, 6830, 6831, 6832, 6833, 6834]),
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
    print([{'id': d['id'], 'reason': d['reason']}
          for d in data['datasetVerifyResult']])


@pytest.mark.parametrize('user, model_id, dataset', [
    # ('c', 333, face_file),
    # ('b', 333, files[:1]),
    # ('b', 330, [image_avif, image_heif, image_no_face, image_too_many_faces]),
    # ('b', 330, files + error_files),
    ('b', 342, files(scarlett)[0:1]),

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
    print([{'id': d['id'], 'reason': d['reason']}
          for d in data['datasetVerifyResult']])
