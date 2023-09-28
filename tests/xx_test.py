import random
import os
from sqlalchemy import select
import pytest
from PIL import Image, ImageOps
import numpy
import face_recognition
from fineai_test.db import Sess
from fineai_test.db.app import UserModel, UploadImageFile
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

def test_pillow_pad():
    image = Image.open('/Users/chensg/Downloads/891.jpg')
    box = (-250, 277, 250, 1000)
    box = (0, 277, 250, 1000)
    cropped_im = ImageOps.pad(image.crop(box), (512, 512), color='red')
    cropped_im.save('/Users/chensg/Downloads/891-2-2.jpg')

def test_pillow_expand():
    image = Image.open('/Users/chensg/Downloads/891.jpg')
    box = (-250, 277, 250, 1000)
    cropped_im = ImageOps.expand(image.crop(box), (50, 0, 0, 20), fill='red')
    cropped_im.save('/Users/chensg/Downloads/891-3.jpg')

def test_pillow_paste():
    image = Image.open('/Users/chensg/Downloads/891.jpg')
    new = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
    # box = (-250, 277, 250, 1000)
    box = (0, 277, 250, 1000)
    new.paste(image.crop(box))
    new.save('/Users/chensg/Downloads/891-5.png')

def expand(box:tuple[int], size:tuple[int], factor:int=1):
    '''
    size: (width, height)

    box: left, upper, right, lower
    centering: ? ?
    '''
    width = box[2] - box[0]
    height = box[3] - box[1]
    w = int(width * factor / 2)
    h = int(height * factor / 2)
    print(f'{w=}, {h=}, {size=}')
    # left = box[0] - w if box[0] - w > 0 else 0
    # upper = box[1] - h if box[1] - h > 0 else 0
    # right = box[2] + w if box[2] + w <= size[0] else size[0]
    # lower = box[3] + h if box[3] + h <= size[1] else size[1]
    left = box[0] - w
    upper = box[1] - h
    right = box[2] + w
    lower = box[3] + h
    box = (
        left if left > 0 else 0,
        upper if upper > 0 else 0,
        right if right < size[0] else size[0],
        lower if lower < size[1] else size[1]
    )
    # fix
    centering = (
       ((box[2] + box[0]) / 2 - (box[2] - box[0]) / 2 ) / (box[2] - box[0]),
       (box[1] + box[3] - 2 * upper) / (lower - upper) / 2, 
    )
    return box, centering

    

def test_pillow_x():
    image = Image.open('/Users/chensg/Pictures/JasonStatham/16206391125879.jpg')
    
    locs = face_recognition.face_locations(numpy.array(image))
    print(locs)
    box = locs[0][3], locs[0][0], locs[0][1], locs[0][2]
    print(f'{box=}')
    box, centering = expand(box, image.size, 2)
    print(f'{box=}, {centering=}')
    cropped = ImageOps.pad(image.crop(box), (512, 512), color='white', centering=centering)
    cropped.save('/Users/chensg/Pictures/JasonStatham/16206391125879-1.jpg')

def test_pillow_y():
    image = Image.open('/Users/chensg/Pictures/JasonStatham/16206391125879.jpg')

    # 定义裁剪区域
    left = -100
    upper = 100
    right = 500
    lower = 500
    box=(614, -199, 1943, 1130)
    left, upper, right, lower = box

    # 进行裁剪
    cropped_image = image.crop((left, upper, right, lower))

    # 定义填充颜色为红色
    fill_color = (255, 0, 0)

    # 计算填充的尺寸
    padding_width = max(0, right - left)
    padding_height = max(0, lower - upper)

    # 进行填充
    padded_image = ImageOps.pad(cropped_image, (padding_width, padding_height), color=fill_color)

    # 保存裁剪后的图像
    padded_image.save('/Users/chensg/Pictures/JasonStatham/16206391125879-3.jpg')


def test_zzz():
    def crop_image(image_path, output_path, x, y, rec_length, margin_ratio, sample_length):
        image = Image.open(image_path)
        #  image.show()
        white = (255, 255, 255)
        #  图像重新缩放，识别的面部区域增加了margin之后，边长缩放到sample_length的对应比例
        resize_ratio = sample_length / (rec_length * (1 + margin_ratio))
        #  原图进行缩放
        image = image.resize((round(image.size[0] * resize_ratio), round(image.size[1] * resize_ratio)))
        #  计算上下左右单边的扩展边长度
        margin_length = round(sample_length * margin_ratio / (1 + margin_ratio) / 2)
        #  创建一个包含扩展边长度的底板
        margin_image = Image.new('RGB', (image.size[0] + margin_length * 2, image.size[1] + margin_length * 2), white)
        #  将缩放后的原图，粘贴到含扩展边底板的中间，在裁剪靠近边缘时，会截取到扩展边的白色区域
        margin_image.paste(image,
                        (0 + margin_length, 0 + margin_length, image.size[0] + margin_length,
                            image.size[1] + margin_length))
        # margin_image.show()
        # 计算缩放后原图中，识别出的脸部位置坐标
        resized_x = round(x * resize_ratio)
        resized_y = round(y * resize_ratio)
        # 裁剪出sample_length长度的方形脸部区域
        cropped_image = margin_image.crop((resized_x, resized_y, resized_x + sample_length, resized_y + sample_length))
        cropped_image.show()
        cropped_image.save(output_path)
    image_path = "/Users/chensg/Pictures/6286fe3bd99fb.jpeg"
    output_path = "/Users/chensg/Pictures/cropped.jpg"
    # x = 378  # 原图中脸部识别的起始横坐标
    # y = 437  # 原图中脸部识别的起始横坐标
    # rec_length = 787 - 378  # 原图中的脸部识别方形的边长，需要判断是不是大于等于face_limit像素，小于的话，判定不合格
    
    # 
    # box = ()
    # x = box[0]
    # y = box[1]
    # rec_length = box[2] - box[0]
    # face location
    box = (268, 798, 397, 669)
    box = (402, 1405, 510, 1298)
    box = (59, 460, 122, 398)
    x = box[3]
    y = box[0]
    rec_length = box[2] - box[0]
    margin_ratio = 25  # 对识别部分扩展边的比例，比如margin_ratio为0.6，则在识别的脸部区域上下左右各增加0.3倍原区域边长的margin，总边长变为1.6倍
    sample_length = 512  # 标准方形样本边长
    # face_limit = math.ceil(sample_length / (1+margin_ratio))
    crop_image(image_path, output_path, x, y, rec_length, margin_ratio, sample_length)

def test_pillow_format():
    im = Image.open('/Users/chensg/Pictures/WechatIMG340.jpeg')
    print(im.format)

def test_aaa():
    # import json
    # urls = ["vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/66cb5412-08ec-4e81-817d-adf71773e5a7.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/803c40ce-3db5-439e-b9aa-0add23d969d9.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/47d929ff-86e5-4378-9fa7-672e677eb552.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/8e8af1b9-f602-496f-b53e-4cd2cee4e6a5.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/8521388f-34cd-4d7f-8fb6-a3467831686c.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/2fc8c00a-2d3e-470f-bd3e-693ccb555d9c.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/7f805051-87cf-443e-9250-f983061295c3.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/fe12a93f-2214-4f4e-934b-6b4e9d9e74f4.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/452a9f2a-eeee-4b18-a83b-c2182e07376d.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/0f63aeab-a0ed-45a0-8b1c-b991c8c50443.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/9c9d1d49-818b-454b-87a3-a07f2b0f4a43.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/f4020d06-4260-4332-8424-bb9f0f3113d6.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/a9f41bdb-0b2a-465a-954c-3ddf8305f6c3.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/f497344f-9da4-443e-956d-df21eff1716f.JPG","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/e7dbc2f7-891f-4a0a-b784-fc4ee39d7339.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/0ac1939b-6028-4d1d-9223-640800f8d159.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/b7eccecf-9509-442b-ba29-a4106e6db515.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/b66c247e-cc5f-4836-87da-a6a5c68c3985.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/e2003358-452d-4bc6-bfb8-901f62294ed3.jpg","vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/88865a14-16b2-4319-b164-1efe35d8972c.jpg",]
    # ids = ["104395","104396","104397","104398","104399","104400","104401","104402","104403","104404","104405","104406","104407","104408","104409","104410","104411","104412","104413","104414",]
    # print(json.dumps([{"no": id, "uri": uri} for id, uri in zip(ids, urls)]))

    # data = [{"no": "105564", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/66cb5412-08ec-4e81-817d-adf71773e5a7.jpg"}, {"no": "104396", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/803c40ce-3db5-439e-b9aa-0add23d969d9.jpg"}, {"no": "104397", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/47d929ff-86e5-4378-9fa7-672e677eb552.jpg"}, {"no": "104398", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/8e8af1b9-f602-496f-b53e-4cd2cee4e6a5.JPG"}, {"no": "104399", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/8521388f-34cd-4d7f-8fb6-a3467831686c.JPG"}, {"no": "104400", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/2fc8c00a-2d3e-470f-bd3e-693ccb555d9c.JPG"}, {"no": "104401", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/7f805051-87cf-443e-9250-f983061295c3.JPG"}, {"no": "104402", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/fe12a93f-2214-4f4e-934b-6b4e9d9e74f4.JPG"}, {"no": "104403", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/452a9f2a-eeee-4b18-a83b-c2182e07376d.JPG"}, {"no": "104404", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/0f63aeab-a0ed-45a0-8b1c-b991c8c50443.jpg"}, {"no": "104405", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/9c9d1d49-818b-454b-87a3-a07f2b0f4a43.JPG"}, {"no": "104406", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/f4020d06-4260-4332-8424-bb9f0f3113d6.jpg"}, {"no": "104407", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/a9f41bdb-0b2a-465a-954c-3ddf8305f6c3.JPG"}, {"no": "104408", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/f497344f-9da4-443e-956d-df21eff1716f.JPG"}, {"no": "104409", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/e7dbc2f7-891f-4a0a-b784-fc4ee39d7339.jpg"}, {"no": "104410", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/0ac1939b-6028-4d1d-9223-640800f8d159.jpg"}, {"no": "104411", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/b7eccecf-9509-442b-ba29-a4106e6db515.jpg"}, {"no": "104412", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/b66c247e-cc5f-4836-87da-a6a5c68c3985.jpg"}, {"no": "104413", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/e2003358-452d-4bc6-bfb8-901f62294ed3.jpg"}, {"no": "104414", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/88865a14-16b2-4319-b164-1efe35d8972c.jpg"}]
    # for line in data:
    #     print(f'update upload_image_file set path=\'{line["uri"]}\' where id={line["no"]};')
    from fineai_task_schema.uri import URI
    a = 'http://c.cc/abc.jpg'
    b = 'vs3://c.cc/path/abc'
    for s in (a, b):
        print('.'.join(s.split('.')[0:-1] + ['png']))
        