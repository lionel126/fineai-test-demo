# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# import asyncio
from sqlalchemy import select
from fineai_test.db import Sess
from fineai_test.db.app import UploadImageFile, Job
from fineai_test.utils.utils import to_url, key_to_url, file_name
from fineai_test.utils import s3


async def get_images_by_job(job_id):
    async with Sess() as sess:
        stmt = select(UploadImageFile).where(UploadImageFile.job_id == job_id)
        rs = await sess.execute(stmt)
        # return [row._mapping['UploadImageFile'] for row in rs.all()]
        return [row[0] for row in rs.all()]

# async def compare_job_results(job_id1, job_id2):
#     async with Sess() as sess:
#         stmt1 = select(UploadImageFile).where(UploadImageFile.job_id==job_id1)
#         stmt2 = select(UploadImageFile).where(UploadImageFile.job_id==job_id2)
#         rs1 = await sess.execute(stmt1)
#         rs2 = await sess.execute(stmt2)
#         job1 = {row[0].path:row[0] for row in rs1.all()}
#         job2 = {row[0].path:row[0] for row in rs2.all()}

#     vs_set = set(job1) & set(job2)
#     job1_set = set(job1) - set(job2)
#     job2_set = set(job2) - set(job1)
#     vs_list = [(job1[path], job2[path]) for path in vs_set]
#     job1_list = [job1[path] for path in job1_set]
#     job2_list = [job2[path] for path in job2_set]
#     for j in vs_list:
#         j[0].path = to_url(j[0].path)
#         # j[1].path = to_url(j[1].path)
#     for j in job1_list:
#         j.path = to_url(j.path)
#     for j in job2_list:
#         j.path = to_url(j.path)
#     return {
#         "vs_list": vs_list,
#         "job1_list": job1_list,
#         "job2_list": job2_list
#     }


async def compare_job_results(job_id1, job_id2):

    async def get_result(s, job_id):
        stmt = select(Job.result).where(Job.id == job_id,
                                        Job.job_kind == 'dataset_verify')
        rs = await s.execute(stmt)
        if row := rs.one_or_none():
            return row[0]['extras'] if row[0] else {}
        return {}

    async with Sess() as sess:
        # tasks = []
        # for job_id in (job_id1, job_id2):
        #     tasks.append(get_result(sess, job_id))
        # job1, job2 = await asyncio.gather(*tasks)
        j1 = await get_result(sess, job_id1)
        j2 = await get_result(sess, job_id2)
        job1_uri = to_url(j1['uri']['uri']) if j1 else ""
        job2_uri = to_url(j2['uri']['uri']) if j2 else ""
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
        "job1_uri": job1_uri,
        "job2_uri": job2_uri,
        "vs_list": vs_list,
        "job1_list": job1_list,
        "job2_list": job2_list
    }


async def get_model(model_id, job_id=None):
    async with Sess() as sess:
        stmt = select(UploadImageFile).where(
            UploadImageFile.user_model_id == model_id).order_by(UploadImageFile.id)
        rs = (await sess.execute(stmt)).all()
        images = [r[0] for r in rs]
        for img in images:
            img.url = to_url(img.path)

        jobs = None
        stmt = select(Job).where(Job.user_model_id == model_id).order_by(Job.created_time.desc())
        jobs = [job[0] for job in (await sess.execute(stmt)).all()]

        if not job_id:
            lora_jobs = [job for job in jobs if job.job_kind == 'lora_train']
            if lora_jobs:
                job_id = lora_jobs[0].id
        
        if job_id:
            lora_job = await get_lora_job(job_id)
            count = 0
            for image in images:
                for img in lora_job['images']:
                    if str(image.id) == img['no']:
                        count += 1
                        image.uploaded = img['url']
                        image.trained = img['trained_url'] if 'trained_url' in img else ''
                        image.txt = img['txt'] if 'txt' in img else ''
            assert len(lora_job['images']) == count, f"{ len(lora_job['images']) } == {count }"


        ret = {
            "keys": ["id", "url", "job_id", "image_type", "reason", "status", "created_time", "uploaded", "trained", "txt"],
            "images": images,
            "job_keys": ["id", "job_kind", 
                        #   "params", "result", 
                          "priority", "status", 
                          "is_delete", "created_time", "theme_param"],
            "jobs": jobs
        }
        # print(ret)
        return ret


async def get_lora_job(job_id):
    async with Sess() as sess:
        stmt = select(Job).where(Job.id == job_id)
        rs = (await sess.execute(stmt)).one_or_none()
        if rs:
            if rs[0].status == 'success':
                params_images_list = [(file_name(image['uri']), image)
                                      for image in rs[0].params['images']]
                params_images = dict(params_images_list)
                assert len(params_images_list) == len(params_images)
                training_images = {file_name(
                    img['key']): img for img in rs[0].result['extras']['training_resources'] if img['kind'] == 'image'}
                training_txt = {}
                for img in rs[0].result['extras']['training_resources']:
                    if img['kind'] == 'txt':
                        # no region in data, so fix it
                        s3c = s3.get_s3_client(img['vendor'], 'cn-beijing')
                        txt = s3c.get_object(Bucket=img['bucket'], Key=img['key'])
                        training_txt[file_name(img['key'])] = str(txt['Body'].read(), 'utf8')
                
                assert len(training_images) == len(params_images)
                assert set(params_images) - set(training_images) == set(
                ), f'{set(params_images) - set(training_images)}'
                assert set(training_images) - set(params_images) == set(
                ), f'{set(training_images) - set(params_images)}'

                combined = [{**params_images[key], **training_images[key], "txt": training_txt[key]}
                            for key in params_images]
                combined.sort(key=lambda it: it['no'])
                
                for img in combined:
                    img['url'] = to_url(img['uri'])
                    img['trained_url'] = key_to_url(img['key'], img['bucket'])
                return {
                    "status": rs[0].status,
                    "images": combined
                }
            else:
                # assert rs[0].params['images'] == rs[0].result['extras']['images']
                images = rs[0].params['images']
                for img in images:
                    img['url'] = to_url(img['uri'])
                return {
                    "status": rs[0].status,
                    "images": images,
                    "message": rs[0].result['message'] if rs[0].result else ""
                }
