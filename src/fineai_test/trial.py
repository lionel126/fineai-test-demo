# not working
# todo

# rye add sqlakeyset
import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, update, case
from fastapi_pagination import add_pagination
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlalchemy import paginate, AsyncConn
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from fineai_test.db import Sess
from fineai_test.db.app import UploadImageFile, Job, UserModel, OutputImageFile, UserJobImage, UserBaseInfo
from fineai_test.utils.utils import to_url, key_to_url, file_name, model_to_dict

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
