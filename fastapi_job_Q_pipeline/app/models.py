from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    enabled_stages: Optional[List[str]] = Field(
        default=None,
        description="List of stages to run. Default runs all stages.",
    )
    order: Optional[List[str]] = Field(
        default=None,
        description="Explicit sequential order of stages.",
    )
    parallel_groups: Optional[List[List[str]]] = Field(
        default=None,
        description="List of parallel stage groups run in order.",
    )


class JobCreateResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
