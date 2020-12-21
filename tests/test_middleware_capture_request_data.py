import unittest
from unittest.mock import Mock

from at_gcp_logging.middleware import CaptureRequestData
from at_gcp_logging import thread_request_context
from tests import helpers


class TestMiddlewareCaptureRequestData(unittest.TestCase):

    def tearDown(self):
        thread_request_context.purge_request_context()

    def test_capture_request_context(self):
        req = helpers.get_request_mock()
        middleware = CaptureRequestData()
        middleware.process_request(req)
        captured_data = thread_request_context.get_request_context()
        assert len(captured_data)
        assert captured_data['user'] == helpers.TEST_USER
        assert captured_data['ip'] == helpers.TEST_IP
        assert captured_data['requested_path'] == helpers.TEST_PATH
        assert captured_data['method'] == helpers.TEST_METHOD
        assert captured_data['user_agent'] == helpers.TEST_AGENT

    def test_clean_request_context(self):
        req = helpers.get_request_mock()
        middleware = CaptureRequestData()
        middleware.process_request(req)
        middleware.process_response(req, Mock())
        captured_data = thread_request_context.get_request_context()
        assert len(captured_data) == 0
