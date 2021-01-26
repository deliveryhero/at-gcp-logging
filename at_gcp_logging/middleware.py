import json
import logging
from http import HTTPStatus

from django.utils import timezone

from at_gcp_logging import thread_request_context


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


class CaptureRequestData:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_request_context.set_request_context(
            user=request.headers.get('user') or getattr(request.user, 'username', 'anonymous'),
            ip=_get_client_ip(request),
            requested_path=request.get_full_path(),
            method=request.META.get('REQUEST_METHOD'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )

        response = self.get_response(request)

        self._cleanup()
        return response

    def process_exception(self, request, exception):
        self._cleanup()

    def _cleanup(self):
        thread_request_context.purge_request_context()


class LogRequestsGCP:
    def __init__(self, get_response):
        self.get_response = get_response
        self._logger = logging.getLogger(self.__class__.__name__)
        self._request_start_time = None

    def __call__(self, request):
        self._logger.info('Received request')
        self._request_start_time = timezone.now()

        response = self.get_response(request)

        self._log_request(response.status_code)
        return response

    def process_exception(self, request, exception):
        self._log_request(HTTPStatus.INTERNAL_SERVER_ERROR)

    def _log_request(self, status_code):
        td = timezone.now() - self._request_start_time
        td_in_ms = td.seconds * 1000 + td.microseconds / 1000
        payload = {
            'message': 'Request finished',
            'duration_ms': td_in_ms,
            'status': status_code
        }
        self._logger.info(json.dumps(payload))
