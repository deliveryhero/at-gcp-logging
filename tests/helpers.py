import logging
from unittest.mock import Mock

from at_gcp_logging.formatter import GCPJSONFormatter


TEST_IP = '127.0.0.1'
TEST_USER = 'usermane'
TEST_METHOD = 'GET'
TEST_AGENT = 'Mock Agent'
TEST_PATH = '/test/path/?param=test'


def get_request_mock():
    req = Mock()
    req.headers = {
        'user': TEST_USER
    }
    req.META = {
        'HTTP_X_FORWARDED_FOR': TEST_IP,
        'REQUEST_METHOD': TEST_METHOD,
        'HTTP_USER_AGENT': TEST_AGENT
    }
    req.get_full_path = Mock(return_value=TEST_PATH)
    return req


def get_logger(name, stream, **kwargs):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream)
    formatter = GCPJSONFormatter(**kwargs)
    handler.setFormatter(formatter)
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(handler)
    return logger, handler
