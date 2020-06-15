import logging
import traceback

import requests
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger('videostore')


class ApiExceptionHandler:
    @classmethod
    def calculate_http_status(cls, exception):
        http_response_code = requests.codes.SERVER_ERROR

        if hasattr(exception, 'status_code'):
            http_response_code = exception.status_code
        elif hasattr(exception, 'code'):
            http_response_code = exception.code
        else:
            if isinstance(exception, IntegrityError):
                http_response_code = requests.codes.BAD_REQUEST
            elif isinstance(exception, ValidationError):
                http_response_code = requests.codes.BAD_REQUEST
        #     TODO - Add more exception types if/when needed

        return http_response_code

    @classmethod
    def calculate_message(cls, exception, message=None):
        if exception and isinstance(exception, IntegrityError):
            # Try to get original message from SQLAlchemy exception
            # Since this exception is adapter speciffic, following will work
            # only for PostgreSQL adapter
            pg_orig = getattr(exception, 'orig', None)
            if pg_orig:
                # pgcode = getattr(pg_orig, 'pgcode', None)
                diag = getattr(pg_orig, 'diag', None)
                if diag:
                    # message = getattr(diag, 'message_detail', '')
                    message = getattr(diag, 'message_primary', '')

        if (
            exception and
            hasattr(exception, 'description') and
            exception.description
        ):
            return exception.description

        return (
            message or
            (str(exception) if exception else '') or
            ''
        ).replace('"', "'")


def build_and_log_error_dict(exception, message=None):
    """Builds error dictionary form exception and optional message."""
    exception_dict = {
        'class': (
            type(exception).__name__ if exception else "None"
        )
    }

    if isinstance(exception, ValidationError):
        exception_dict['errors'] = exception.messages
        exception_dict['message'] = 'Found some validation errors in your request. Cowardly refusing to continue!'
    else:
        exception_dict['message'] = ApiExceptionHandler.calculate_message(exception, message)

    logger.critical(traceback.format_exc())

    return exception_dict

def build_error_response(exception):
    """
    Builds JSON response from error dictionary.
    """
    response = jsonify(build_and_log_error_dict(exception))
    response.status_code = ApiExceptionHandler.calculate_http_status(exception)
    return response
