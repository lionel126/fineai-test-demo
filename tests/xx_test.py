import random
from sqlalchemy import select
from requests import request
import pytest
from api.config import settings
from fineai_test.db import Sess
from fineai_test.db.app import UserModel, UploadImageFile
# from locust.contrib.csvreader import CSVReader
from locust_plugins.csvreader import CSVReader


@pytest.mark.asyncio
async def test_1():
    async with Sess() as sess:
        stmt = select(UserModel).where(UserModel.status.in_(('train', 'finish')), UserModel.id > 1333, UserModel.user_id == 12).order_by(UserModel.id)
        rs = await sess.execute(stmt)
        ids = [r[0].id for r in rs.all()]
        err = {}
        with open('.data', 'w') as f:
            for idx, mid in enumerate(ids):
                stmt_images = select(UploadImageFile).where(UploadImageFile.user_model_id == mid, UploadImageFile.is_delete == False)
                rs_images = await sess.execute(stmt_images)
                rows = rs_images.all()
                uri = [r[0].id for r in rows if r[0].image_type == 'face_detection'][0]
                images = [r[0].id for r in rows if r[0].image_type == 'dataset_verify' and r[0].status == 'checked']
                if len(images) < 20:
                    err[mid] = len(images)
                # images_str = ','.join(map(str, images))
                images2 = [r[0].id for r in rows if r[0].image_type == 'dataset_verify' and r[0].status != 'checked']
                # images2_str = ','.join(map(str, images2))
                images_str = ','.join(map(str, random.sample(images, 25 if len(images) >= 25 else len(images)) + random.sample(images2, 5 if len(images2) >= 5 else len(images2))))
                f.write(f'{mid},{uri},{images_str}')
                if idx < len(ids) - 1:
                    f.write('\n')
        print(err)


def test_resurge():
    from locustfile import resurge
    resurge(43169)