from .config import settings
from .session import Session

s = Session(settings.task_base_url)

def get_payload(task_no, name, output, uri, images, priority=5):
    payload = {
        "config": {
            "noise_offset": "0",
            "repeats": 12,
            "remove_bg_fill_color": "#ffffff",
            "lr": "0.0002",
            "save_every_n_epochs": 10,
            "output": "vs3://cn-beijing/fineai-secure/xw-dev/model/lora/32/2506",
            "keep_tokens": 0,
            "pretrained_model_uri": "vs3: //cn-beijing/fineai-test/models/majicmixRealistic_betterV2V25.safetensors",
            "min_bucket_reso": 256,
            "min_snr_gamma": 0,
            "face_points_weight": 0.9,
            "is_v2_model": 0,
            "max_train_epoches": 10,
            "height": 512,
            "max_bucket_reso": 1024,
            "batch_size": 2,
            "persistent_data_loader_workers": 0,
            "parameterization": 0,
            "train_text_encoder_only": 0,
            "stop_text_encoder_training": 0,
            "lr_restart_cycles": 1,
            "network_dim": 128,
            "unet_lr": "0.0002",
            "entropy_points_weight": 0.15,
            "corner_points_weight": 0.23,
            "lr_warmup_steps": 0,
            "lr_scheduler": "cosine_with_restarts",
            "caption_text": f"1girl, white background, {name}",
            "network_alpha": 128,
            "width": 512,
            "name": "vGedZqOxO8lryxwD",
            "train_unet_only": 0,
            "optimizer_type": "AdamW8bit",
            "text_encoder_lr": "1e-5",
            "clip_skip": 2
        },
        "images": [
            {
                "no": "104719",
                "uri": "vs3://cn-beijing/fineai-secure/xw-dev/cropped/32/2506/dataset_verify/88b33be6-6c6a-4a51-976a-796b6ef180d1.jpeg"
            },
        ],
        "priority": 5,
        "source": "xw_job",
        "task_no": "1e865d81-380e-4871-8484-e948508a18b3",
        "uri": "vs3: //cn-beijing/fineai-secure/xw-dev/cropped/32/2506/face_detection/a46f552c-e45f-481a-9310-580911bb3818.webp"
    }
    payload['priority'] = priority
    payload['task_no'] = task_no
    payload['uri'] = uri
    payload['images'] = images
    payload['config']['output'] = output
    payload['config']['name'] = name
    return payload

def train(json):
    path = 'lora_train'
    return s.post(path, json=json)

def detect_face(json):
    path = 'lora_face_detection'
    return s.post(path, json=json)

def verify_dataset(json):
    path = 'lora_dataset_verify'
    return s.post(path, json=json)