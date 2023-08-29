import logging
from .main import app # noqa

logging.basicConfig(
    # format='%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s',
    format='%(asctime)s %(levelname)s %(name)s %(module)s:%(lineno)d - %(message)s',
    force=True,
)
logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger().addFilter(logging.Filter(__package__))
# logging.getLogger(__package__).setLevel(logging.DEBUG)
