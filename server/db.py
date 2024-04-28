import os
import urllib.parse

import asyncpg

from server import metrics_asyncpg

dsn = os.environ.get('POSTGRES_DSN', 'postgresql://root:root@127.0.0.1:8432/test')
min_size = 5
max_size = 10
max_queries = 100
max_inactive_connection_lifetime = 5


async def create_pool() -> asyncpg.Pool:
    metrics_asyncpg.POOL_MIN_SIZE.labels(addr=_get_addr()).set(min_size)
    metrics_asyncpg.POOL_MAX_SIZE.labels(addr=_get_addr()).set(max_size)

    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=min_size,
        max_size=max_size,
        max_queries=max_queries,
        max_inactive_connection_lifetime=max_inactive_connection_lifetime,
        connection_class=metrics_asyncpg.WrapperConnection,
    )


def track_pool_idle_size(pool: asyncpg.Pool):
    metrics_asyncpg.POOL_IDLE_SIZE.labels(addr=_get_addr()).set(pool.get_idle_size())


def _get_addr() -> str:
    parsed: urllib.parse.ParseResult = urllib.parse.urlparse(dsn)
    return f'{parsed.hostname}:{parsed.port}'
