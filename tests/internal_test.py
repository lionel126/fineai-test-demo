import pytest
from api.server_internal import Internal

@pytest.mark.parametrize('model_id', [
    2623
])
def test_generate_avatar(model_id):
    Internal().generate_avatar(model_id)

# def test_train():
#     Internal().train()