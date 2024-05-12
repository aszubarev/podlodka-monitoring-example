import time

import prometheus_client
from prometheus_client import Counter, Gauge, Histogram
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match

from server.utils import powers_of

prometheus_client.disable_created_metrics()


REQUESTS = Counter(
    name="starlette_requests_total",
    documentation="Total count of requests by method and path.",
    labelnames=["method", "path_template"],
)
REQUESTS_IN_PROGRESS = Gauge(
    name="starlette_requests_in_progress",
    documentation="Gauge of requests by method and path currently being processed.",
    labelnames=["method", "path_template"],
)
REQUESTS_PROCESSING_TIME = Histogram(
    name="starlette_requests_processing_time",
    documentation="Histogram of requests processing time by path (in seconds).",
    labelnames=["method", "path_template"],
)
RESPONSES = Counter(
    name="starlette_responses_total",
    documentation="Total count of responses by method, path and status codes.",
    labelnames=["method", "path_template", "status_code"],
)
RESPONSES_BYTES = Histogram(
    name="starlette_responses_bytes",
    documentation="Histogram of responses by body size.",
    labelnames=["method", "path_template"],
    buckets=powers_of(2, 30),
)
EXCEPTIONS = Counter(
    name="starlette_exceptions_total",
    documentation="Histogram of exceptions raised by method, path and exception type",
    labelnames=["method", "path_template", "exception_type"],
)


class PrometheusMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        path_template = self.get_path_template(request)

        REQUESTS.labels(method=method, path_template=path_template).inc()
        REQUESTS_IN_PROGRESS.labels(method=method, path_template=path_template).inc()

        before_time = time.time()

        try:
            response: Response = await call_next(request)
        except Exception as e:
            EXCEPTIONS.labels(method=method, path_template=path_template, exception_type=type(e).__name__).inc()
            raise e from None
        else:
            RESPONSES.labels(
                method=method,
                path_template=path_template,
                status_code=response.status_code,
            ).inc()
            RESPONSES_BYTES.labels(
                method=method,
                path_template=path_template,
            ).observe(self.get_content_length(response))
        finally:
            processing_time = time.time() - before_time

            REQUESTS_IN_PROGRESS.labels(method=method, path_template=path_template).dec()
            REQUESTS_PROCESSING_TIME.labels(method=method, path_template=path_template).observe(processing_time)

        return response

    @classmethod
    def get_path_template(cls, request: Request) -> str:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path
        return 'not_found'

    @classmethod
    def get_content_length(cls, response: Response) -> float:
        return float(response.headers.get('content-length', 0))
