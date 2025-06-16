from typing import Any
from tracker.models import RequestLogs
class RequestLoggingMiddleware:
    """
    Middleware to log incoming requests.
    """

    def __init__(self, get_response)->None:
        self.get_response = get_response

    def __call__(self, request):
        request_info=request
        print(request_info)
        RequestLogs.objects.create(
            request_info=vars(request_info),
            request_type=request_info.method,
            request_method=request_info.path
        )

        return self.get_response(request)