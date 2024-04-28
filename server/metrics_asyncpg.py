import time

from asyncpg import Connection
from prometheus_client import Counter, Histogram, Gauge, Info

QUERIES = Counter(
    name="asyncpg_queries_total",
    documentation="Total count of queries by addr.",
    labelnames=["addr"],
)
QUERIES_PROCESSING_TIME = Histogram(
    name="asyncpg_queries_processing_time_seconds",
    documentation="Histogram of queries processing time by addr (in seconds).",
    labelnames=["addr"],
)
EXCEPTIONS = Counter(
    name="asyncpg_exceptions_total",
    documentation="Histogram of exceptions raised by addr and exception type.",
    labelnames=["addr", "exception_type"],
)
CONNECTIONS = Gauge(
    name="asyncpg_connections",
    documentation="Gauge of connections by addr.",
    labelnames=["addr"],
)
CONNECTIONS_NEW = Counter(
    name="asyncpg_connections_new_total",
    documentation="Counter of created connections by addr.",
    labelnames=["addr"],
)
POOL_IDLE_SIZE = Gauge(
    name="asyncpg_pool_idle_size",
    documentation="Gauge of idle pool size by addr.",
    labelnames=["addr"],
)
POOL_MIN_SIZE = Gauge(
    name="asyncpg_pool_min_size",
    documentation="Gauge of min pool size by addr.",
    labelnames=["addr"],
)
POOL_MAX_SIZE = Gauge(
    name="asyncpg_pool_max_size",
    documentation="Gauge of max pool size by addr.",
    labelnames=["addr"],
)


class WrapperConnection(Connection):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CONNECTIONS.labels(addr=self.addr).inc()
        CONNECTIONS_NEW.labels(addr=self.addr).inc()

    def __del__(self):
        super().__del__()
        CONNECTIONS.labels(addr=self.addr).dec()

    async def _do_execute(self, *args, **kwargs):
        QUERIES.labels(addr=self.addr).inc()
        before_time = time.time()
        try:
            return await super()._do_execute(*args, **kwargs)
        except Exception as e:
            exception_type = type(e).__name__
            EXCEPTIONS.labels(addr=self.addr, exception_type=exception_type).inc()
            raise e from None
        finally:
            after_time = time.time()
            processing_time = after_time - before_time
            QUERIES_PROCESSING_TIME.labels(addr=self.addr).observe(processing_time)

    @property
    def addr(self) -> str:
        host, port = self._addr
        return f'{host}:{port}'
