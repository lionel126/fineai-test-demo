import logging
from .config import settings
from .main import app # noqa

logging.basicConfig(
    # format='%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s',
    format='%(asctime)s %(levelname)s %(name)s %(module)s:%(lineno)d - %(message)s',
    force=True,
)
logging.getLogger(__name__).setLevel(settings.log_level)