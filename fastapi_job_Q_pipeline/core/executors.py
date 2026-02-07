from __future__ import annotations

from typing import Any, Dict, Optional

from core.pipeline import Pipeline
from core.stages import Stage1LoadAndNormalize, Stage2CpuTransform, Stage3WriteOutput


class PipelineExecutor:
    def __init__(self) -> None:
        stages = {
            Stage1LoadAndNormalize.name: Stage1LoadAndNormalize(),
            Stage2CpuTransform.name: Stage2CpuTransform(),
            Stage3WriteOutput.name: Stage3WriteOutput(),
        }
        self.pipeline = Pipeline(stages)

    def run(
        self,
        context: Dict[str, Any],
        enabled: Optional[list[str]] = None,
        order: Optional[list[str]] = None,
        parallel_groups: Optional[list[list[str]]] = None,
    ) -> Dict[str, Any]:
        if enabled is None:
            enabled = list(self.pipeline.stages.keys())
        return self.pipeline.run(context, enabled, order, parallel_groups)
