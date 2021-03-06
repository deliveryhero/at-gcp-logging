import unittest
from io import StringIO
import json

from tests.helpers import get_logger


class TestFormatter(unittest.TestCase):

    def test_logger_default_params(self):
        stream = StringIO()
        logger, handler = get_logger('test_logger_default_params', stream)
        logger.info('test')
        handler.flush()
        record = json.loads(stream.getvalue())
        assert record['message'] == 'test'
        assert record['level'] == 'INFO'
        assert record['name'] == 'test_logger_default_params'
        assert 'exc_info' in record
        assert 'stack_info' in record

    def test_logger_default_params_json_msg(self):
        stream = StringIO()
        logger, handler = get_logger('test_logger_default_params', stream)
        logger.info('{"json_data": "test"}')
        handler.flush()
        record = json.loads(stream.getvalue())
        assert record['json_data'] == 'test'

    def test_logger_custom_params(self):
        stream = StringIO()
        format_dict = {
            'test_key': 'message'
        }
        logger, handler = get_logger('test_logger_custom_params', stream,
                                     format_dict=format_dict)
        test_msg = 'test msg'
        logger.info(test_msg)
        handler.flush()
        record = json.loads(stream.getvalue())
        assert record['test_key'] == test_msg

    def test_logger_format_exception(self):
        stream = StringIO()
        logger, handler = get_logger('test_logger_format_exception', stream)
        try:
            1/0
        except Exception as e:
            logger.exception(e)
        handler.flush()
        record = json.loads(stream.getvalue())
        assert 'ZeroDivisionError: division by zero' in record['exc_info']
        assert record['level'] == 'ERROR'
