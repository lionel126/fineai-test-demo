from functools import cache

import boto3
from fineai_test.config import settings

@cache  # noqa: B019
def get_s3_client(vendor: str, region: str):
    config = settings.get_bucket(vendor, region)
    if config is None:
        raise ValueError(f"{vendor} region {region} not found")

    s3 = boto3.client(
        's3',
        aws_access_key_id=config.access_key,
        aws_secret_access_key=config.secret_key,
        endpoint_url=config.endpoint,
        config=boto3.session.Config(
            s3={
                'addressing_style': config.addressing_style,
            },
            signature_version=config.signature_version,
        ),
    )
    return s3