import face_recognition
from fineai_test.utils.utils import to_url, jwt_token


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