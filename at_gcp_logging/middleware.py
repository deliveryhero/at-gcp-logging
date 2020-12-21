from at_gcp_logging import thread_request_context


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


class CaptureRequestData:

    def process_request(self, request):
        thread_request_context.set_request_context(
            user=request.headers['user'],
            ip=_get_client_ip(request),
            requested_path=request.get_full_path(),
            method=request.META.get('REQUEST_METHOD'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )

    def process_response(self, request, response):
        thread_request_context.purge_request_context()
