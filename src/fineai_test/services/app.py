# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio
from sqlalchemy import insert, update, select
from fineai_test.db import Sess
from fineai_test.db.app import UploadImageFile, Job
from fineai_test.utils.utils import to_url

async def get_images_by_job(job_id):
    async with Sess() as sess:
        stmt = select(UploadImageFile).where(UploadImageFile.job_id==job_id)
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
        stmt = select(Job.result).where(Job.id==job_id)
        rs = await s.execute(stmt)
        if row:=rs.one_or_none():
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
        job1_images = {ret['no']:ret for ret in j1['images']} if j1 else {}
        job2_images = {ret['no']:ret for ret in j2['images']} if j2 else {}

    vs_set = set(job1_images) & set(job2_images)
    job1_set = set(job1_images) - set(job2_images)
    job2_set = set(job2_images) - set(job1_images)
    vs_list = [(job1_images[no], job2_images[no], 'different' if job1_images[no]['message'] != job2_images[no]['message'] else 'same') for no in vs_set]
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