from __future__ import annotations

import redis

from app.settings import settings


_redis_pool = redis.ConnectionPool.from_url(settings.redis_url, decode_responses=True)


def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=_redis_pool)
