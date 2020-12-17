import logging
import unittest
from io import StringIO
import json

from at_gcp_logging.formatter import GCPJSONFormatter


class TestFormatter(unittest.TestCase):

    def _get_logger(self, name, stream, **kwargs):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(stream)
        formatter = GCPJSONFormatter(**kwargs)
        handler.setFormatter(formatter)
        for h in logger.handlers:
            logger.removeHandler(h)
        logger.addHandler(handler)
        return logger, handler

    def test_logger_default_params(self):
        stream = StringIO()
        logger, handler = self._get_logger('test_logger_default_params', stream)
        logger.info('test')
        handler.flush()
        record = json.loads(stream.getvalue())
        assert record['message'] == 'test'
        assert record['level'] == 'INFO'
        assert record['name'] == 'test_logger_default_params'
        assert 'exc_info' in record
        assert 'stack_info' in record

    def test_logger_custom_params(self):
        stream = StringIO()
        format_dict = {
            'test_key': 'message'
        }
        logger, handler = self._get_logger('test_logger_custom_params', stream,
                                           format_dict=format_dict)
        test_msg = 'test msg'
        logger.info(test_msg)
        handler.flush()
        record = json.loads(stream.getvalue())
        assert record['test_key'] == test_msg

    def test_logger_format_exception(self):
        stream = StringIO()
        logger, handler = self._get_logger('test_logger_format_exception', stream)
        try:
            1/0
        except Exception as e:
            logger.exception(e)
        handler.flush()
        record = json.loads(stream.getvalue())
        assert 'ZeroDivisionError: division by zero' in record['exc_info']
        assert record['level'] == 'ERROR'
