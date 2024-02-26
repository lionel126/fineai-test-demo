import random
import os
from sqlalchemy import select
import pytest
import pytest_asyncio
from fineai_test.db import Sess
from fineai_test.db.app import UserModel, UploadImageFile
from api.utils import jwt_token
from fineai_test.services.app import get_user_info
# from locust.contrib.csvreader import CSVReader


@pytest.mark.asyncio
async def test_1():
    async with Sess() as sess:
        stmt = select(UserModel).where(UserModel.status.in_(('train', 'finish')), UserModel.id > 1333, UserModel.user_id == 12).order_by(UserModel.id)
        rs = await sess.execute(stmt)
        ids = [r[0].id for r in rs.all()]
        err = {}
        with open('.data', 'w') as f:
            for idx, mid in enumerate(ids):
                stmt_images = select(UploadImageFile).where(UploadImageFile.user_model_id == mid, UploadImageFile.is_delete is False)
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

@pytest.mark.asyncio
async def test_2():
    '''dump training data for load testing'''
    async with Sess() as s:
        stmt = select(UserModel).where(UserModel.status.in_(('train', 'finish')), UserModel.user_id == 12).order_by(UserModel.id)
        rs = await s.execute(stmt)
        ids = [r[0].id for r in rs.all()]
        with open('.data', 'w') as f:
            for idx, model_id in enumerate(ids):
                f.write(f'{model_id}')
                if idx < len(ids) - 1:
                    f.write('\n')

def test_3():
    '''split .data to different locust'''
    # 10 locusts, 100 model ids / locust
    count = 100
    amount = 10
    dirs = [os.path.join('..', f'fineai-test{i}') for i in range(amount)]
    with open('.data', 'r') as f:
        lines = f.readlines()
    for d in dirs:
        with open(os.path.join(d, '.data'), 'w') as f:
            f.writelines(lines[:count])
            lines = lines[count:]

def test_zoo():
    from kazoo.client import KazooClient
    zk = KazooClient(hosts='192.168.4.51:2181')
    zk.start()
    children = zk.get_children('/')
    print(children)
    data = zk.get('/xpc/fine/ai/app/dev')
    print(str(data[0], encoding='utf8'))
    zk.stop()

@pytest.mark.asyncio
async def test_jwt_token():
    async with Sess() as db:
        user = await get_user_info(db, 22)
        print(jwt_token(user, 'https://xw.fineai.pro:443'))
        print(jwt_token(user, 'https://xw.fineai.pro:80'))
        # pod内压测 app service, 域名解析到ingress
        print(jwt_token(user, 'https://xw.fineai.pro'))


@pytest_asyncio.fixture
async def async_session():
    # # 创建异步引擎和异步会话
    # async_engine = create_async_engine("your_database_url")
    # async_session = sessionmaker(
    #     async_engine, expire_on_commit=False, class_=AsyncSession
    # )
    from fineai_test.db import Sess, engines
    # 创建会话
    
    async with Sess() as session:
        yield session

    # # 返回会话生成器
    # yield create_session()

    # # 在夹具完成后清理资源
    # async_engine.dispose()
    await engines['app_store'].dispose()

@pytest.mark.asyncio
async def test_async_session(async_session):
    from sqlalchemy import text
    result = await async_session.execute(text("SELECT * FROM user_base"))
    print(result)

