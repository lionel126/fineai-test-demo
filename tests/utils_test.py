from hashids import Hashids
from datetime import datetime
from fineai_test.utils.utils import to_url, jwt_token

def test_url():
    print(to_url("vs3://cn-beijing/fineai-test/xw-dev/upload/8/61/dataset_verify/b4919ada-7bec-4641-a99a-cbb33c187ca2.jpeg"))

def test_jwt():    
    jwt_token()
