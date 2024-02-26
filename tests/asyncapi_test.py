import time
import resource
import random
import logging
from logging.handlers import TimedRotatingFileHandler
from random import sample, choice
import pytest
import pytest_asyncio
import asyncio
from api.asyncapp import App, uploads
# from api_test import daddario, scarlett
from api.utils import files
from api.config import settings
from fineai_test.services.app import get_dataset_images, pay
from fineai_test.services.mq import connect
from fineai_test.db import Sess

log = logging.getLogger(__name__)
handler = TimedRotatingFileHandler('logs/test.log', when='midnight')
format = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s')
handler.setFormatter(format)
log.addHandler(handler)
log.setLevel(logging.DEBUG)


@pytest_asyncio.fixture
async def db():
    async with Sess() as s:
        yield s


@pytest.mark.parametrize('uid, model_id, face, dataset, update, train', [
    # ('d', 2667, choice(files(settings.daddario)), files(settings.daddario), {'modelName': 'daddario'}, True),
    ('d', 2670, None, files('/Users/chensg/Pictures/dilraba/',
     exclude=['4dc73d7b-ae38-4e00-a938-bc5cef908e67.jpg']), {'modelName': 'dilraba'}, True),

    # ('d', 2662, files(settings.scarlett)[0], files(settings.scarlett)[1:33], {'modelName': 'scar'}, True),
    # ('d', None, files(settings.scarlett)[0], None, {'modelName': 'scar'}, True),
    # ('e', None, files(scarlett)[0], files(scarlett)[1:33], {'modelName': 'scar'}, True),

])
@pytest.mark.asyncio
async def test_train(db, uid, model_id, face, dataset, update, train):
    params = {'_priority': 1}
    async with await App(uid) as app:
        include_previous_images = False
        if model_id and face is not None:
            include_previous_images = True

        ts = []
        ts.append(time.time())
        if not model_id:
            model_id = (await (await app.create_model()).json())['data']['id']
        log.debug(f'{model_id=}')
        model_name = f'{model_id}-{update.pop("modelName")}' if (
            update and 'modelName' in update) else f'{model_id}-'
        await app.update_model(id=model_id, modelName=model_name, **update if update else {})

        # 正脸
        ts.append(time.time())
        if face:
            log.debug(f'{model_id=} face detection started')
            if isinstance(face, str):
                json = {"modelId": model_id, "fileName": face}
                data = (await (await app.create_face(json)).json())['data']
                log.debug(f'{model_id=} face before uploading')
                ts.append(time.time())
                await uploads([data,])
                ts.append(time.time())
                log.debug(f'{model_id=} face after uploaded')
                image_id = data['id']
            else:
                # isinstance(face, int)
                image_id = face

            job_id = (await (await app.finish_face({"imageId": image_id, "modelId": model_id})).json())[
                'data']['jobId']
            times = 30
            while data := (await (await app.job_state(job_id)).json())['data']:

                if data['status'] != 'success':
                    times -= 1
                    if times < 0:
                        log.debug(f'{model_id=} face detection not finished')
                        return
                    await asyncio.sleep(1)
                    continue

                # if data['faceDetectionResult']['status'] != 'checked':
                #     return
                if data['faceDetectionResult']['status'] == 'checked':
                    break
                else:
                    log.debug(f'{model_id=} face detection failed')
                    return

        # 补充
        # if dataset:
        # face合格后上传
        ts.append(time.time())
        if dataset is not None:
            # None: ignore
            # []: redo with previous images
            log.debug(f'{model_id=} dataset verify started')
            ids = [image.id for image in await get_dataset_images(db, model_id) if image.status == 'invalid'] if include_previous_images else []
            if len(ids) < 200:
                images = []
                for file in dataset:
                    if isinstance(file, int):
                        ids.append(file)
                    else:
                        # isinstance(file, str)
                        images.append(file)

                if images:
                    fs = (await (await app.create_dataset(model_id, images)).json())['data']
                    log.debug(f'{model_id=} dataset before uploading')
                    ts.append(time.time())
                    await uploads(fs)
                    ts.append(time.time())
                    log.debug(f'{model_id=} dataset after uploaded')
                    for f in fs:
                        # await upload(f['fileName'], f['host'], f['uploadParam'])
                        ids.append(f['id'])

            if len(ids) > 200:
                ids = sample(ids, k=200)
            job_id = (await (await app.finish_dataset(model_id, ids)).json())['data']['jobId']
            times = 60
            while (await (await app.job_state(job_id)).json())['data']['status'] != 'success':
                times -= 1
                if times < 0:
                    log.debug(f'{model_id=} finish dataset not finished')
                    break
                await asyncio.sleep(1)
        ts.append(time.time())
        if train:
            await pay(db, model_id)
            res = await app.train(model_id, params=params)
            ret = await res.json()
            ts.append(time.time())
            log.debug(f'{model_id=} {ret=}')
        log.debug(
            f'{model_id=}:{[ts[i+1]-ts[i] for i in range(len(ts)) if i < len(ts) - 1]}')


@pytest.mark.parametrize('uid, model_id, face, dataset, update, train', [
    # ('c', None, choice(files(scarlett)), files(scarlett), {'modelName': 'scar'}, True),
    # ('c', None, choice(files(daddario)), files(daddario), {'modelName': 'daddario'}, True),

    ('c', None, choice(files(settings.daddario)), files(settings.daddario), {
     'modelName': 'daddario', 'gender': choice(['female', 'male'])}, True),
])
@pytest.mark.asyncio
async def test_keep_training(uid, model_id, face, dataset, update, train):

    connection, _, queue = connect()
    count = queue.method.message_count
    connection.close()

    if count > 0:
        return

    log.debug('train >>>>> ' * 10)
    await test_train(uid, model_id, face, dataset, update, train)


@pytest.mark.asyncio
async def test_train_concurrently():
    soft_limit = settings.max_memory * 1024 * 1024 * 1024
    hard_limit = settings.max_memory * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit, hard_limit))

    async def run():
        while True:
            await test_train('a', None, choice(files(settings.daddario)), files(settings.daddario), {'modelName': 'daddario'}, True)

    # async def run2():
    #     tasks = [run() for _ in range(2)]
    #     await asyncio.gather(*tasks)

    # def main():
    #     # loop = asyncio.new_event_loop()
    #     loop = asyncio.get_event_loop()
    #     asyncio.set_event_loop(loop)
    #     try:
    #         loop.run_until_complete(run2())
    #     finally:
    #         loop.close()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as exe:
    #     futures = [exe.submit(main()) for _ in range(2)]
    #     ret = concurrent.futures.as_completed(futures)
    #     # await asyncio.sleep(3600 * 10)

    for _ in range(5):
        asyncio.create_task(run())
    await asyncio.sleep(3600 * 10)

    # tasks = [run() for _ in range(2)]
    # await asyncio.gather(*tasks)


@pytest.mark.parametrize('uid, modelId', [
    ('b', 1284),
])
@pytest.mark.asyncio
async def test_pay(uid, modelId):
    async with await App(uid) as app:
        await app.create_order(modelId=modelId, price=3)


@pytest.mark.parametrize('uid, modelId', [
    ('d', 2662),
])
@pytest.mark.asyncio
async def test_output(uid, modelId):
    themes = ((7, 1), (9, 1), (9, 2), (9, 3), (8, 1), (8, 2))
    async with await App(uid) as app:
        tasks = []
        for _ in range(10):
            params = {'_priority': 1}
            themeId, themeModelId = random.choice(themes)
            tasks.append(app.output_portray(
                params=params, modelId=modelId, themeId=themeId, themeModelId=themeModelId))
        await asyncio.gather(*tasks)


@pytest.mark.parametrize('uid, modelId, imageId', [
    ('e', 2632, 10733),
])
@pytest.mark.asyncio
async def test_output_hd(uid, modelId, imageId):
    async with await App(uid) as app:
        await app.output_hd(modelId=modelId, imageId=imageId)


@pytest.mark.parametrize('uid, modelId', [
    ('c', 2504),
])
@pytest.mark.asyncio
async def test_output_list(uid, modelId):
    count = 0
    async with await App(uid) as app:
        createdTime = 0
        while True:
            data = (await (await app.output_list(modelId, createdTime=createdTime)).json())['data']
            length = len(data)
            print(f'{length=}')
            if length == 0:
                break
            count += length
            createdTime = data[-1]['createdTime']

    print(f'{count=}')


@pytest.mark.parametrize('uid, modelId', [
    ('c', 2504),
])
@pytest.mark.asyncio
async def test_favorite(uid, modelId):
    async with await App(uid) as app:
        data = (await (await app.output_list(modelId)).json())['data']
        for out in data:
            images = (await (await app.output_detail(out['id'])).json())['data']['images']
            for im in images:
                await app.favorite(imageId=im['id'], modelId=modelId)


@pytest.mark.parametrize('uid, modelId', [
    ('d', 2584),
])
@pytest.mark.asyncio
async def test_clear_dataset(uid, modelId):
    async with await App(uid) as app:
        data = (await (await app.dataset_list(modelId)).json())['data']
        for image_id in [d['id'] for d in data]:
            await app.delete_image(image_id)
