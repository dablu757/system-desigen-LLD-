from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

import redis


class RedisJobRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def create_job(self, job_id: str, data: Dict[str, Any]) -> None:
        now = int(time.time())
        payload = {
            "status": "QUEUED",
            "created_at": now,
            "updated_at": now,
            **data,
        }
        self.redis.hset(f"job:{job_id}", mapping=self._serialize(payload))

    def update_job(self, job_id: str, data: Dict[str, Any]) -> None:
        payload = {"updated_at": int(time.time()), **data}
        self.redis.hset(f"job:{job_id}", mapping=self._serialize(payload))

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        raw = self.redis.hgetall(f"job:{job_id}")
        if not raw:
            return None
        return self._deserialize(raw)

    def _serialize(self, data: Dict[str, Any]) -> Dict[str, str]:
        payload: Dict[str, str] = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                payload[key] = json.dumps(value)
            elif value is None:
                payload[key] = ""
            else:
                payload[key] = str(value)
        return payload

    def _deserialize(self, data: Dict[str, str]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        for key, value in data.items():
            if value == "":
                payload[key] = None
                continue
            if key in {"pipeline_config", "result"}:
                payload[key] = json.loads(value)
                continue
            if key in {"created_at", "updated_at"}:
                payload[key] = int(value)
                continue
            payload[key] = value
        return payload
