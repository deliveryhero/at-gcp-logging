import json
import unittest
from io import StringIO

from at_gcp_logging import thread_request_context
from at_gcp_logging.middleware import CaptureRequestData
from tests import helpers


class TestLoggingWithMiddleware(unittest.TestCase):

    def tearDown(self):
        thread_request_context.purge_request_context()

    def test_request_context_captured(self):
        req = helpers.get_request_mock()
        middleware = CaptureRequestData()
        middleware.process_request(req)
        stream = StringIO()
        logger, handler = helpers.get_logger('test_request_context_captured', stream)
        logger.info('test')
        handler.flush()
        record = json.loads(stream.getvalue())
        assert record['user'] == helpers.TEST_USER
        assert record['ip'] == helpers.TEST_IP
        assert record['requested_path'] == helpers.TEST_PATH
        assert record['method'] == helpers.TEST_METHOD
        assert record['user_agent'] == helpers.TEST_AGENT
