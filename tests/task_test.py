import pytest
from api.task import train, get_payload, detect_face, verify_dataset

@pytest.mark.parametrize('json', [
    get_payload('1e865d81-380e-4871-8484-e948508a18b4', '001', 'vs3://cn-beijing/fineai-secure/xw-dev/model/lora/32/2506', '', [])
])
def test_train(json):
    train(json)


def test_detect_face():
    json = {
        "task_no": "81b74e0d-ef96-43a3-9a28-3f0aa51532ac",
        "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/face_detection/6f93fbc8-78ee-4cbc-9007-d759968ee1ab.JPG",
        "priority": 5,
        "source": "xw_job"
    }
    detect_face(json)

def test_verify_dataset():
    json = {
        "task_no": "8e087dd9-9913-4b76-8b8f-79794a94f59c",
        "source": "xw_job",
        "priority": 5,
        "tolerance": 0.5,
        "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/face_detection/6f93fbc8-78ee-4cbc-9007-d759968ee1ab.JPG",
        "images": [{"no": "105564", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/66cb5412-08ec-4e81-817d-adf71773e5a7.jpg"}, {"no": "104396", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/803c40ce-3db5-439e-b9aa-0add23d969d9.jpg"}, {"no": "104397", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/47d929ff-86e5-4378-9fa7-672e677eb552.jpg"}, {"no": "104398", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/8e8af1b9-f602-496f-b53e-4cd2cee4e6a5.JPG"}, {"no": "104399", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/8521388f-34cd-4d7f-8fb6-a3467831686c.JPG"}, {"no": "104400", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/2fc8c00a-2d3e-470f-bd3e-693ccb555d9c.JPG"}, {"no": "104401", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/7f805051-87cf-443e-9250-f983061295c3.JPG"}, {"no": "104402", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/fe12a93f-2214-4f4e-934b-6b4e9d9e74f4.JPG"}, {"no": "104403", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/452a9f2a-eeee-4b18-a83b-c2182e07376d.JPG"}, {"no": "104404", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/0f63aeab-a0ed-45a0-8b1c-b991c8c50443.jpg"}, {"no": "104405", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/9c9d1d49-818b-454b-87a3-a07f2b0f4a43.JPG"}, {"no": "104406", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/f4020d06-4260-4332-8424-bb9f0f3113d6.jpg"}, {"no": "104407", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/a9f41bdb-0b2a-465a-954c-3ddf8305f6c3.JPG"}, {"no": "104408", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/f497344f-9da4-443e-956d-df21eff1716f.JPG"}, {"no": "104409", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/e7dbc2f7-891f-4a0a-b784-fc4ee39d7339.jpg"}, {"no": "104410", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/0ac1939b-6028-4d1d-9223-640800f8d159.jpg"}, {"no": "104411", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/b7eccecf-9509-442b-ba29-a4106e6db515.jpg"}, {"no": "104412", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/b66c247e-cc5f-4836-87da-a6a5c68c3985.jpg"}, {"no": "104413", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/e2003358-452d-4bc6-bfb8-901f62294ed3.jpg"}, {"no": "104414", "uri": "vs3://cn-beijing/fineai-secure/xw-dev/upload/37/2508/dataset_verify/88865a14-16b2-4319-b164-1efe35d8972c.jpg"}]
    }
    verify_dataset(json)