import json
import logging

from at_gcp_logging import thread_request_context


class GCPJSONFormatter(logging.Formatter):

    def __init__(self, format_dict=None, **kwargs):
        default_format = {
            'message': 'message'
        }
        self._format_dict = format_dict if format_dict is not None else default_format
        super().__init__(**kwargs)

    def _add_user_defined_fields_to_record(self, res, record):
        for res_key, record_key in self._format_dict.items():
            try:
                val = record.__dict__[record_key]
            except KeyError:
                raise KeyError(f'"{record_key}" is not valid formatted attribute')
            res[res_key] = val

    def _add_default_fields_to_record(self, res, record):
        res.update({
            'asctime': self.formatTime(record, self.datefmt),
            'name': record.name,
            'severity': record.levelname,
            'pathname': record.pathname,
            'lineno': record.lineno,
            'thread': record.thread,
            'pid': record.process,
            'exc_info': '' if not record.exc_info else self.formatException(record.exc_info),
            'stack_info': '' if not record.stack_info else self.formatStack(record.stack_info)
        })
        res.update(**thread_request_context.get_request_context())

    def format(self, record):
        super(GCPJSONFormatter, self).format(record)
        res = {}
        self._add_default_fields_to_record(res, record)
        self._add_user_defined_fields_to_record(res, record)
        return json.dumps(res)
