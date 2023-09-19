# not working
# todo

# rye add sqlakeyset
from fastapi import APIRouter
from sqlalchemy import select
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlalchemy import paginate

from fineai_test.db import Sess
from fineai_test.db.app import Job

router = APIRouter(prefix='/api')

@router.get('/jobs')
async def get_jobs() -> CursorPage:
    async with Sess() as sess:
        stmt = select(Job)
        # if kw:
        #     for k, v in kw.items():
        #         if v:
        #             stmt = stmt.where(getattr(Job, k) == v)
        stmt = stmt.order_by(Job.created_time.desc())
        p = await paginate(sess, stmt)

    # return p
    return {
        'keys': ['id', 'user_model_id', 'job_kind', 'priority'],
        **{k: getattr(p, k) for k in p}
    }
