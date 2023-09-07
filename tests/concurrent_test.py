import time
from random import sample, choice
import pytest
from api.asyncapp import App, upload, uploads
from api.session import AsyncSession
from api.config import settings
from api_test import scarlett, daddario
from api_test import pics
from fineai_test.services.app import get_dataset_images

@pytest.mark.parametrize('uid, model_id, face, dataset, update, train', [
    # ('c', None, choice(pics(scarlett)), pics(scarlett), {'modelName': 'scar'}, True),
    # ('c', None, choice(pics(daddario)), pics(daddario), {'modelName': 'daddario'}, True),

    ('c', None, choice(pics(daddario)), pics(daddario), {'modelName': 'daddario'}, True),
])
@pytest.mark.asyncio
async def test_train(uid, model_id, face, dataset, update, train):
    async with await App(uid) as app:
        include_previous_images = False
        if model_id:
            include_previous_images = True
        
        if not model_id:
            model_id = (await (await app.create_model()).json())['data']['id']
        
        model_name = f'{model_id}-{update.pop("modelName")}' if (update and 'modelName' in update) else f'{model_id}-'
        await app.update_model(id=model_id, modelName=model_name, **update if update else {})

        # 正脸
        if face:
            if isinstance(face, str):
                json = {"modelId": model_id, "fileName": face}
                data = (await (await app.create_face(json)).json())['data']
                # await upload(face, data['host'], data['uploadParam'])
                await uploads([data,])
                image_id = data['id']
            else: 
                # isinstance(face, int)
                image_id = face
            

            job_id = (await (await app.finish_face({"imageId": image_id, "modelId": model_id})).json())[
                'data']['jobId']
            
            while data:=(await (await app.job_state(job_id)).json())['data']:
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
            ids = [image.id for image in await get_dataset_images(model_id) if image.status == 'invalid'] if include_previous_images else []
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
                    await uploads(fs)
                    for f in fs:
                        # await upload(f['fileName'], f['host'], f['uploadParam'])
                        ids.append(f['id'])                    
            if len(ids) > 200:
                ids = sample(ids, k=200)
            job_id = (await (await app.finish_dataset(model_id, ids)).json())['data']['jobId']
            print(f'dataset job: {job_id}')        
            while (await (await app.job_state(job_id)).json())['data']['status'] != 'success':
                time.sleep(1)
        
        if train:
            await app.train(model_id)

