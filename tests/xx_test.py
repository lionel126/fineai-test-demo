from requests import request
import pytest
import face_recognition
from api.app import App
from api.config import settings


def test_compare():
    pics =  [
        '/Users/chensg/Downloads/60f6998a-3fd5-4bc0-9827-bae3312fea61.png',
        '/Users/chensg/Downloads/a41c6b26-1adf-45c3-b24d-38940b0badda.jpeg',
        # '/Users/chensg/Pictures/Alexandra Daddario/0457f991c5d17bde63a10a18ad56052a.jpg', 
        # '/Users/chensg/Pictures/Alexandra Daddario/1b7131abe7284690a1e349878a5eeaae.bmp',
        # '/Users/chensg/Pictures/Alexandra Daddario/6MM4MAHRVFMEPLJYQHVTH5WCPI.jpg'
    ]
    encodings = []
    for p in pics:
        im = face_recognition.load_image_file(p)
        encodings.append(face_recognition.face_encodings(im)[0])
    
    
    ret = face_recognition.compare_faces(encodings, encodings[0])
    print(f'{ret=}')
    distance = face_recognition.face_distance(encodings, encodings[0])
    print(f'{distance=}')

@pytest.mark.asyncio
async def test_yyy():
    # app = await App('c')
    app = await App(14)
    app.output_portray(modelId=401, themeId=1, themeModelId=1)


def test_zzz():
    js = '''[
            {
                "favorite": null,
                "hasHd": null,
                "id": 15599,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/f4e77388-345c-4a5a-bf3c-4e771c4b0396.avif~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "图片无法识别",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15600,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/eb67c667-9d72-453c-b879-0f51b5de7e57.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15601,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/f1cecd35-f800-4a2f-9d2c-952a2be15670.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "识别到多张人脸",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15602,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/d7678c98-ef90-4c34-828c-b61165eae532.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15603,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/05e5080b-d7fd-4d1f-a45a-7c913d072887.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15604,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/2023596a-adeb-43f2-a990-3e4285d7d3d5.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15605,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/82fcba33-51ab-4864-8973-33f4b65b79f3.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15606,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/efb89b1c-5bd7-48d7-be15-6c87910b3f5c.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15607,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/14e08230-f703-47f4-a37a-69bd752cc809.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15578,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/add7f493-e7f1-4ee7-8aa6-50b5311541a8.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15579,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/65fd46b2-a9ae-457f-8ee3-f122d7c8925e.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15580,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/738135e6-923d-4397-9bf6-a2f8e9099834.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15581,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/e002cca1-8d22-4230-84b5-3f735607d1f0.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15582,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/5a661c62-7e08-42c0-a81a-8ade72508503.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "识别到多张人脸",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15583,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/efab51af-6bb8-47f3-ae1e-4024228139ce.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15584,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/151b8867-5e3b-47a7-8a7e-c0d8f913c18b.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15585,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/c69436be-7916-40c2-9660-7f870b8151f7.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15587,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/bc6131eb-33d5-4663-b627-6d36f54296de.DS_Store~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "图片无法识别",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15588,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/aa6abb0b-c37f-4013-aa50-9ba00622684c.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15589,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/0c68caf2-8f8f-462b-afb9-9ccab154a023.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15590,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/4e4b194b-0ed3-43aa-990b-9e0c0a485263.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15591,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/528329a8-6dc9-4586-a62d-70b30992ac96.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15592,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/107ead67-baff-42c5-b231-a95b5bc39626.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15593,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/66af14ab-9cd4-41a0-8bb5-7ace99168c9d.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15596,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/f0207212-400d-4e7e-8079-2c4f75a6f2cf.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15586,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/bcb63d6c-c682-4a31-819b-6ec3fa098abf.webp~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15620,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/90b45098-d637-4c3e-b7db-f150a14a81c1.jpg_large~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15621,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/5b8088b1-07c0-46f8-ab5b-55c206b5f0ff.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15622,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/8cabc12a-6cac-4bce-9899-8349ca9936e8.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15623,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/ddb74130-e4a0-4407-b903-bb4fb71cd1d2.webp~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15624,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/8978850d-3a86-4de2-8a1e-00bc6c649022.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15594,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/24cf0274-dbe3-4ced-a531-c0ca14daf309.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15597,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/fc160a47-9f32-48e5-90aa-46649c0b76e8.bmp~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15598,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/028c3a11-b7a5-4909-bde8-3bc4433652cc.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15609,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/22a2a156-bd56-4dc7-8df4-3abe8ff00e41.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15610,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/fcdab7d4-b0c7-4200-ac2b-e0e3a78b5662.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15617,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/7c71a79c-a6f0-460c-8625-2e0d62432311.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15618,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/c527321d-b613-4ee8-b5b9-d146c787960c.webp~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15608,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/e11f5267-4791-40a5-b19c-c70bd7c01adb.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15611,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/3838ff4d-8c65-4df0-9a5b-b6de44f0806f.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15613,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/8935f158-cc3b-40ef-a802-190fe6ad4a49.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "识别到多张人脸",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15614,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/30a911a7-7372-4bd2-9447-0e8cff0ce0c7.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15615,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/2e047b45-a8e1-4a0b-b0cb-b364249d99a4.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15616,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/c3e34743-5fe3-4555-ad10-adac3945b98e.webp~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "不是同一个人",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15619,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/f14e5da7-6077-48a3-b099-984548da74b4.avif~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "图片无法识别",
                "status": "invalid"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15625,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/de22bda8-18a1-4666-acec-97835bcde634.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15626,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/4844d776-ed15-4a2d-831f-a4651e137dd5.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15627,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/f5f6c8d1-4370-45fd-8682-db92e62a928c.jpeg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15628,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/e9400ed4-bd7c-4c37-99ad-9e8bbb553311.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            },
            {
                "favorite": null,
                "hasHd": null,
                "id": 15629,
                "imageType": "dataset_verify",
                "imageUrl": "https://fineai-secure0.xpccdn.com/xw-dev/upload/18/555/dataset_verify/c36654b8-e069-4288-bc7c-039a02123e96.jpg~tplv-5x3rixm6so-watermark-v1.image",
                "reason": "ok",
                "status": "checked"
            }
        ]'''
    import json
    print([it['id'] for it in json.loads(js)])
    print([it['id'] for it in json.loads(js) if it['status'] == 'checked'])
    print([it['id'] for it in json.loads(js) if it['status'] == 'invalid'])


cert = settings.REQUESTS_CA_BUNDLE
proxies = {'http': settings.http_proxy, 'https': settings.https_proxy}

def test_mq():
    tasks = [
        '38563706-8d23-4748-9505-1cd2b29ee14c',
        '24176e75-f572-4424-9424-fedfeb6126a1',
        '671a6f05-c85f-4526-ab2c-6381b2e7ca4f'
    ]
    request('post', 'http://192.168.103.101:8000/consume', json=tasks, proxies=proxies, verify=cert)
    # consume(**json)