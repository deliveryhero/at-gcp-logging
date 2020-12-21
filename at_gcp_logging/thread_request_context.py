import threading


_thread_context = threading.local()


def set_request_context(**ctx):
    if getattr(_thread_context, 'request_data', None) is None:
        _thread_context.request_data = {}
    _thread_context.request_data.update(**ctx)


def get_request_context():
    return getattr(_thread_context, 'request_data', {})


def purge_request_context():
    if getattr(_thread_context, 'request_data', None) is not None:
        del _thread_context.request_data
