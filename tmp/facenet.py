import os
import torch
from torchvision import transforms
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

daddario = '/Users/chensg/Pictures/scarlettJohansson'

pics = [os.path.join(daddario, f) for f in os.listdir(daddario)]

# 加载预训练的 FaceNet 模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# 加载 MTCNN 模型用于人脸检测和对齐
mtcnn = MTCNN()

# 转换图像的预处理
transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# 批量照片路径列表
batch_photo_paths = pics[1:33]

# 单张照片路径
single_photo_path = pics[0]

print(batch_photo_paths)
print(single_photo_path)

# 加载批量照片并提取人脸特征向量
batch_features = []
for photo_path in batch_photo_paths:
    try:
        img = Image.open(photo_path).convert('RGB')
        img_cropped = mtcnn(img)
        img_cropped = img_cropped.squeeze().detach().cpu().numpy()
        img_cropped = img_cropped.transpose(1, 2, 0)
        # img_cropped = Image.fromarray(img_cropped)
        img_cropped = Image.fromarray((img_cropped * 255).astype('uint8'))
        img_tensor = transform(img_cropped).unsqueeze(0).to(device)
        with torch.no_grad():
            features = model(img_tensor)
    except Exception as err:
        features = err
    batch_features.append(features)

# 加载单张照片并提取人脸特征向量
img_single = Image.open(single_photo_path).convert('RGB')
img_single_cropped = mtcnn(img_single)
img_single_cropped = img_single_cropped.squeeze().detach().cpu().numpy()
img_single_cropped = img_single_cropped.transpose(1, 2, 0)
img_single_cropped = Image.fromarray((img_single_cropped * 255).astype('uint8'))
img_single_tensor = transform(img_single_cropped).unsqueeze(0).to(device)
with torch.no_grad():
    single_features = model(img_single_tensor)

# 计算相似度并判断是否为同一个人
threshold = 0.7  # 相似度阈值
for idx, features in enumerate(batch_features):
    if isinstance(features, Exception):
        print(batch_photo_paths[idx], features)
    else:
        similarity = torch.nn.functional.cosine_similarity(features, single_features)
        print(batch_photo_paths[idx], similarity)
    # if similarity > threshold:
    #     print("Same person")
    # else:
    #     print("Different person")
