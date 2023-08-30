import face_recognition
from fineai_test.utils.utils import to_url, jwt_token

def test_url():
    print(to_url("vs3://cn-beijing/fineai-test/xw-dev/upload/8/61/dataset_verify/b4919ada-7bec-4641-a99a-cbb33c187ca2.jpeg"))

def test_jwt():    
    jwt_token()


def test_compare():
    im1 = face_recognition.load_image_file('/Users/chensg/Pictures/Alexandra Daddario/1b7131abe7284690a1e349878a5eeaae.bmp')
    im2 = face_recognition.load_image_file('/Users/chensg/Pictures/Alexandra Daddario/6MM4MAHRVFMEPLJYQHVTH5WCPI.jpg')
    known = face_recognition.face_encodings(im1)
    to_check = face_recognition.face_encodings(im2)[0]
    ret = face_recognition.compare_faces(known, to_check)
    print(ret)
    distance = face_recognition.face_distance(known, to_check)[0]
    print(f'{distance=}')