import logging

log = logging.getLogger(__name__)

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



def model_to_dict(model):
    return {k: getattr(model, k) for k in model.__table__.columns.keys()}
