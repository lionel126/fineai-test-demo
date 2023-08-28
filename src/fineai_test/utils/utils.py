from hashids import Hashids
import hashlib
import jwt


def to_url(s3uri: str):
    if 'fineai-test' in s3uri:
        template = '~tplv-pvyy2n7wp8-chensg-test.image'
        url = s3uri.replace('vs3://cn-beijing/fineai-test',
                            'https://image0-fineai-test.xpccdn.com')
    elif 'fineai-secure' in s3uri:
        template = '~tplv-5x3rixm6so-watermark-v1:0:0:q100.image'
        url = s3uri.replace('vs3://cn-beijing/fineai-secure',
                            'https://fineai-secure0.xpccdn.com')
    else:
        return s3uri
    return f'{url}{template}'
    # url = urlparse(s3uri)
    # url = url._replace(scheme='https')
    # url = url._replace(netloc='image0-fineai-test.xpccdn.com')
    # url = url._replace(path=url.path.replace('/fineai-test', '') + '~tplv-pvyy2n7wp8-chensg-test.image')
    # return url.geturl()

# def uri_to_key(s3uri:str):
#     return s3uri.replace('vs3://cn-beijing/fineai-test/', '')


def file_name(uri: str):
    return uri.split('/')[-1].split('.')[0]


def key_to_url(key, bucket='fineai-test'):
    if bucket == 'fineai-test':
        return f'https://image0-fineai-test.xpccdn.com/{key}~tplv-pvyy2n7wp8-chensg-test.image'
    elif bucket == 'fineai-secure':
        return f'https://fineai-secure0.xpccdn.com/{key}~tplv-5x3rixm6so-watermark-v1:0:0:q100.image'


def jwt_token(iss='http://192.168.103.101:9090'):
    user_id = 1
    open_id = 'csgoA_WQ63tqac75U0iL6tIUWYQhmow'
    union_id = 'csgoIRU76zO7uMhAy3wCV0Y49F5De5k'
    # :csgoIRU76zO7uMhAy3wCV0Y49F5De5k:csgoA_WQ63tqac75U0iL6tIUWYQhmow'
    app_id = 'wxee64f42a910fe3e6'

    login_user_key = hashlib.md5(
        bytes(f'{app_id}:{union_id}:{open_id}', 'utf-8')).digest().hex()
    sub = "XW IT Co."
    # exp = datetime.now()
    salt = 'xinPC_MA@2023'
    h = Hashids(salt=salt, min_length=16)

    payload = {"unionId": h.encode(
        user_id), "sub": sub, "iss": iss, "login_user_key": login_user_key}
    # print(payload)
    encoded_jwt = jwt.encode(payload, open_id, algorithm="HS256")
    return encoded_jwt
