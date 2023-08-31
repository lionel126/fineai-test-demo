import pytest
from api.server_internal import Internal

@pytest.mark.parametrize('model_id', [
    82, 
    120, 
    124, 
    149, 
    174, 
    181, 
    182, 
    183, 
    185, 
    186,
    187,
    189, 
    195,
])
def test_generate_avatar(model_id):
    Internal().generate_avatar(model_id)