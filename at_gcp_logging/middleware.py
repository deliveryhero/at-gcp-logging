import json
import logging

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from at_gcp_logging import thread_request_context


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


class CaptureRequestData(MiddlewareMixin):

    def process_request(self, request):
        thread_request_context.set_request_context(
            user=request.headers.get('user') or request.user.username or 'anonymous',
            ip=_get_client_ip(request),
            requested_path=request.get_full_path(),
            method=request.META.get('REQUEST_METHOD'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )

    def process_response(self, request, response):
        thread_request_context.purge_request_context()
        return response


class LogRequestsGCP(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request_start_time = None
        self._logger = logging.getLogger(self.__class__.__name__)

    def process_request(self, request):
        self._logger.info('Received request')
        self._request_start_time = timezone.now()

    def process_response(self, request, response):
        td = timezone.now() - self._request_start_time
        td_in_ms = td.seconds * 1000 + td.microseconds / 1000
        payload = {
            'message': 'Request finished',
            'duration_ms': td_in_ms,
            'status': response.status_code
        }
        self._logger.info(json.dumps(payload))
        return response
