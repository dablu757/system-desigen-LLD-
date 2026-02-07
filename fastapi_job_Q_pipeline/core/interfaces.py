from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Stage(ABC):
    name: str
    depends_on: List[str]

    @abstractmethod
    def run(self, context: Dict[str, Any], results: Dict[str, Any]) -> Any:
        raise NotImplementedError
