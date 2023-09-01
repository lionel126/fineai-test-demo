# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# import asyncio
import logging
from sqlalchemy import select
from fineai_test.db import Sess
from fineai_test.db.app import UploadImageFile, Job, UserModel, OutputImageFile
from fineai_test.utils.utils import to_url, key_to_url, file_name, model_to_dict
from fineai_test.utils import s3

log = logging.getLogger(__name__)

# async def get_models_pagination():
#     s = Sess()
#     stmt = select(UserModel).order_by(UserModel.id.desc())
#     return s, stmt


async def get_models(size=200, page=1):
    async with Sess() as sess:
        stmt = select(UserModel).order_by(UserModel.id.desc()
                                          ).limit(size).offset((page - 1) * size)
        rs = (await sess.execute(stmt)).all()
    models = [model_to_dict(r[0]) for r in rs]

    keys = models[0].keys() if models else []
    return {
        'keys': keys,
        'models': models
    }


async def get_images_by_job(job_id):
    # deprecated
    async with Sess() as sess:
        stmt = select(UploadImageFile).where(UploadImageFile.job_id == job_id)
        rs = await sess.execute(stmt)
        return [row[0] for row in rs.all()]


async def _get_images_by_model(model_id):
    async with Sess() as sess:
        stmt = select(UploadImageFile).where(
            UploadImageFile.user_model_id == model_id)
        rs = await sess.execute(stmt)
        # return [row._mapping['UploadImageFile'] for row in rs.all()]
        return [row[0] for row in rs.all()]

async def _get_output_images_by_job(job_id):
    async with Sess() as sess:
        stmt = select(OutputImageFile).where(OutputImageFile.job_id==job_id)
        rs = await sess.execute(stmt)
        return [row[0] for row in rs.all()]

async def compare_job_results(job_id1, job_id2):
    job1 = await _get_job(job_id1, 'dataset_verify')
    job2 = await _get_job(job_id2, 'dataset_verify') 
    j1 = job1.result['extras']
    j2 = job2.result['extras']
    job1_uri = to_url(j1['uri']['uri']) if job1.status == 'success' else to_url(j1['uri'])
    job2_uri = to_url(j2['uri']['uri']) if job2.status == 'success' else to_url(j2['uri'])
    job1_images = {ret['no']: ret for ret in j1['images']} if j1 else {}
    job2_images = {ret['no']: ret for ret in j2['images']} if j2 else {}

    vs_set = set(job1_images) & set(job2_images)
    job1_set = set(job1_images) - set(job2_images)
    job2_set = set(job2_images) - set(job1_images)
    vs_list = [(job1_images[no], job2_images[no], 'different' if job1_images[no]
                ['message'] != job2_images[no]['message'] else 'same') for no in vs_set]
    job1_list = [job1_images[no] for no in job1_set]
    job2_list = [job2_images[no] for no in job2_set]
    for j in vs_list:
        j[0]['uri'] = to_url(j[0]['uri'])
        j[1]['uri'] = to_url(j[1]['uri'])
    for j in job1_list:
        j['uri'] = to_url(j['uri'])
    for j in job2_list:
        j['uri'] = to_url(j['uri'])
    return {
        "keys": ['no', 'message', 'distance'],
        "job1_uri": job1_uri,
        "job2_uri": job2_uri,
        "vs_list": vs_list,
        "job1_list": job1_list,
        "job2_list": job2_list
    }


async def _get_model(model_id):
    async with Sess() as sess:
        stmt = select(UserModel).where(UserModel.id == model_id)
        row = (await sess.execute(stmt)).one_or_none()
    if row:
        return row[0]


async def get_model_jobs(model_id):
    async with Sess() as sess:
        model = await _get_model(model_id)
        stmt = select(Job).where(Job.user_model_id ==
                                 model_id).order_by(Job.created_time.desc())
        jobs = [job[0] for job in (await sess.execute(stmt)).all()]

        ret = {
            "model": model_to_dict(model),
            "job_keys": ["id", "job_kind",
                         #   "params", "result",
                         "priority", "status",
                         "is_delete", "created_time", "theme_param"],
            "jobs": jobs
        }
        return ret


async def _get_job(job_id, kind=None):
    async with Sess() as sess:
        if kind:
            stmt = select(Job).where(Job.id == job_id, Job.job_kind == kind)
        else:
            stmt = select(Job).where(Job.id == job_id)
        rs = (await sess.execute(stmt)).one_or_none()
    return rs[0]


async def get_lora_result(job_id):
    lora = await _get_job(job_id, kind='lora_train')
    if not lora:
        return

    params_images_list = [(file_name(image['uri']), image)
                          for image in lora.params['images']]
    uri = lora.params['uri']
    params_images_list.append((file_name(uri), {'uri': uri}))
    params_images = dict(params_images_list)
    assert len(params_images_list) == len(params_images)
    if lora.status == 'success':
        training_images = {file_name(
            img['key']): img for img in lora.result['extras']['training_resources'] if img['kind'] == 'image'}

        # assertion: amount of uploaded images == amount of trained images
        try:
            assert len(training_images) == len(
                params_images), f'{len(training_images)=} == {len(params_images)=}'
            assert set(params_images) - set(training_images) == set(
            ), f'{set(params_images) - set(training_images)}'
            assert set(training_images) - set(params_images) == set(
            ), f'{set(training_images) - set(params_images)}'
        except AssertionError as e:
            log.warn(
                f'frontal face image should be uploaded in new lora job: {e}')

        training_txt = {}

        for img in lora.result['extras']['training_resources']:
            if img['kind'] == 'txt':
                # no region in data, so fix it
                s3c = s3.get_s3_client(img['vendor'], 'cn-beijing')
                txt = s3c.get_object(
                    Bucket=img['bucket'], Key=img['key'])
                training_txt[file_name(img['key'])] = str(
                    txt['Body'].read(), 'utf8')

        combined = [{**params_images[key], **training_images[key], "txt": training_txt[key]}
                    for key in training_images]
        for img in combined:
            img['trained_url'] = key_to_url(img['key'], img['bucket'])
    else:
        combined = list(params_images.values())
    combined.sort(key=lambda it: int(it.get('no', 0)))
    for img in combined:
        img['url'] = to_url(img['uri'])
    return {
        "keys": ['id', 'job_kind', 'status', 'priority', 'created_time'],
        "job": lora,
        "images": combined,
    }


async def get_model_lora(model_id, job_id):
    model = await _get_model(model_id)
    images = await _get_images_by_model(model_id)
    for img in images:
        img.url = to_url(img.path)

    job_result = await get_lora_result(job_id)
    job = job_result['job']
    count = 0
    for image in images:
        for img in job_result['images']:
            if img['url'] == image.url:
                count += 1
                image.uploaded = img['url']
                image.trained = img['trained_url'] if 'trained_url' in img else ''
                image.txt = img['txt'] if 'txt' in img else ''
    assert len(job_result['images']
               ) == count, f"{ len(job_result['images']) } == {count }"
    images.sort(key=lambda it: int(it.id))
    ret = {
        "model": model_to_dict(model),
        "job": model_to_dict(job),
        "image_keys": ["id", "url", "job_id", "image_type", "reason", "status", "created_time"],
        "job_keys": ["trained", "txt"],
        "images": images,
    }
    return ret


async def get_model_dataset_verify(model_id, job_id=None):
    model = await _get_model(model_id)
    upload_images = [model_to_dict(img) for img in await _get_images_by_model(model_id)]
    job = await _get_job(job_id, kind='dataset_verify')

    if not job:
        return {
            "model": model_to_dict(model),
            "images": upload_images
        }
    params_images_list = [(file_name(image['uri']), image)
                          for image in job.params['images']]
    uri = job.params['uri']
    params_images_list.append((file_name(uri), {'no': '', 'uri': uri}))
    params_images = dict(params_images_list)
    assert len(params_images_list) == len(params_images)
    if job.status == 'success':
        result_images = {file_name(
            img['uri']): img for img in job.result['extras']['images']}
        uri = job.result['extras']['uri']
        result_images[file_name(uri['uri'])] = uri
        # assertion: amount of uploaded images == amount of verified images
        assert len(result_images) == len(
            params_images), f'{len(result_images)=} == {len(params_images)=}'
        assert set(params_images) - \
            set(result_images) == set(
        ), f'{set(params_images) - set(result_images)}'
        assert set(result_images) - \
            set(params_images) == set(
        ), f'{set(result_images) - set(params_images)}'

        combined = [{**ui, **params_images.get(file_name(ui['path']), {}), **result_images.get(
            file_name(ui['path']), {})} for ui in upload_images]

    else:
        combined = [
            {**ui, **params_images.get(file_name(ui['path']), {})} for ui in upload_images]
    combined.sort(key=lambda it: it['id'])
    for img in combined:
        img['url'] = to_url(img['path'])
    return {
        "model": model_to_dict(model),
        "job": model_to_dict(job),
        "images": combined,
        "image_keys": ["id", "url", "job_id", "image_type", "reason", "status", "created_time", "is_delete"],
        "job_keys": ["distance", "tolerance", "face_count", "success", "message"],
    }


async def get_model_face_detection(model_id, job_id=None):
    model = await _get_model(model_id)
    upload_images = [model_to_dict(img) for img in await _get_images_by_model(model_id)]
    job = await _get_job(job_id, kind='face_detection')

    if not job:
        return {
            "model": model_to_dict(model),
            "images": upload_images
        }
    uri = job.params['uri']
    params_image = {file_name(uri): {'uri': uri}}
    if job.status == 'success':
        result_image = {file_name(uri): job.result['extras']}
        combined = [{**img, **params_image.get(file_name(img['path']), {}), **result_image.get(
            file_name(img['path']), {})} for img in upload_images]
    else:
        combined = [
            {**img, **params_image.get(file_name(img['path']), {})} for img in upload_images]
    for img in combined:
        img['url'] = to_url(img['path'])
    combined.sort(key=lambda it: it['id'])
    return {
        "model": model_to_dict(model),
        "job": model_to_dict(job),
        "images": combined,
        "image_keys": ["id", "url", "job_id", "image_type", "reason", "status", "created_time"],
        "job_keys": ["face_count", "success", "message"],
    }

async def get_model_img2img(model_id, job_id):
    model = await _get_model(model_id)
    job = await _get_job(job_id, kind='img2img')
    images = await _get_output_images_by_job(job_id)
    for img in images:
        img.path = to_url(img.path)
    return {
        "model": model_to_dict(model),
        "job": model_to_dict(job),
        "keys": ["id", "job_id", "image_type", "path", "hd_id", "status", "is_delete", "updated_time", "created_time"],
        "images": [model_to_dict(img) for img in images]
    }
