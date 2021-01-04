at-gcp-logging
===

This package consists of 3 parts:
- Formatter

   Translates messages into proper json format and adds some default data https://github.com/deliveryhero/at-gcp-logging/blob/master/at_gcp_logging/formatter.py#L32

- `at_gcp_logging.middleware.CaptureRequestData` middleware

   Adds to each log entry by default data defined here https://github.com/deliveryhero/at-gcp-logging/blob/master/at_gcp_logging/middleware.py#L20

- `at_gcp_logging.middleware.LogRequestsGCP` middleware

   Logs each request and response with request time in ms and response status. All other request related data is added in middleware above

How to use:
---
```python
MIDDLEWARE = [
    ...,
    'at_gcp_logging.middleware.CaptureRequestData',
    'at_gcp_logging.middleware.LogRequestsGCP',
]

LOGGING = {
    'formatters': {
        'gcp': {
            '()': 'at_gcp_logging.formatter.GCPJSONFormatter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'gcp'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}
```
Optionally you can add additional data to json either in settings:
```python
LOGGING = {
    'formatters': {
        'gcp': {
            '()': 'at_gcp_logging.formatter.GCPJSONFormatter',
            'format_dict': {
                'my-field': 'filename' #  map custom field to any valid attribute https://docs.python.org/3/library/logging.html#logrecord-attributes
            }   
        }
    }
}
```
or format log message as json:
```python
import logging, json
logger = logging.getLogger(__name__)
payload = {
    'message': 'Request finished',
    'duration_ms': 1000,
    'status': response.status_code
}
logger.info(json.dumps(payload))
```
The result will be like this:
```json
{"asctime": "2021-01-04 11:52:19,828", "name": "LogRequestsGCP", "severity": "INFO", "pathname": "/code/at-gcp-logging/at_gcp_logging/middleware.py", "lineno": 53, "thread": 139782117534496, "pid": 7, "exc_info": "", "stack_info": "", "user": "username", "ip": "172.18.0.1", "requested_path": "/api/v1/vendors/3db1cd38-2b44-41e7-8354-d8ff1c853602/carts/active/", "method": "GET", "user_agent": "PostmanRuntime/7.26.8", "message": "Request finished", "duration_ms": 15.895, "status": 200}
```
`duration_ms` and `status` are custom fields here
