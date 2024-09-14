import time
import json
from django.utils.deprecation import MiddlewareMixin

class RequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            end_time = time.time()
            duration = end_time - request.start_time

            log_data = {
                "user": str(request.user) if request.user.is_authenticated else "Anonymous",
                "method": request.method,
                "path": request.get_full_path(),
                "status_code": response.status_code,
                "start_time": request.start_time,
                "end_time": end_time,
                "duration": duration,
            }

            with open('logs/request_response_log.json', 'a') as f:
                f.write(json.dumps(log_data) + '\n')

        return response
