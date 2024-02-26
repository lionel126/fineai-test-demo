import os
import logging
from hashids import Hashids
import hashlib
import jwt

log = logging.getLogger(__name__)

def jwt_token(user, iss='http://192.168.103.101:9090'):
    # user_info_id = 1
    # openid = 'csgoA_WQ63tqac75U0iL6tIUWYQhmow'
    # union_id = 'csgoIRU76zO7uMhAy3wCV0Y49F5De5k'
    # app_id = 'wxee64f42a910fe3e6'

    # user = settings.get_usr(uid)

    login_user_key = hashlib.md5(
        bytes(f'{user.app_id}:{user.union_id}:{user.openid}', 'utf-8')).digest().hex()
    sub = "XW IT Co."
    # exp = datetime.now()
    salt = 'xinPC_MA@2023'
    h = Hashids(salt=salt, min_length=16)

    payload = {"unionId": h.encode(
        user.id), "sub": sub, "iss": iss, "login_user_key": login_user_key}
    log.debug(f'{user}, {payload=}, {user.openid=}')
    encoded_jwt = jwt.encode(payload, user.openid, algorithm="HS256")
    return encoded_jwt

def files(directory, exclude:None|list=None):
    
    return [os.path.join(directory, f) for f in os.listdir(directory) if not exclude or f not in exclude]