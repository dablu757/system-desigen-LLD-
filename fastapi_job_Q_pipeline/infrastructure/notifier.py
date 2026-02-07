from __future__ import annotations

from typing import Any, Dict, Optional

import requests


class HttpCallbackNotifier:
    def notify(self, callback_url: Optional[str], job_id: str, payload: Dict[str, Any]) -> None:
        if not callback_url:
            return
        try:
            requests.post(
                callback_url,
                json={"job_id": job_id, "payload": payload},
                timeout=10,
            )
        except Exception:
            return
