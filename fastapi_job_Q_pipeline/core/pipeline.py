from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from core.interfaces import Stage


class PipelineError(Exception):
    pass


class Pipeline:
    def __init__(self, stages: Dict[str, Stage]):
        self.stages = stages

    def _validate_stages(self, enabled: List[str]) -> None:
        missing = [name for name in enabled if name not in self.stages]
        if missing:
            raise PipelineError(f"Unknown stages: {missing}")

        for name in enabled:
            deps = self.stages[name].depends_on
            for dep in deps:
                if dep not in enabled:
                    raise PipelineError(f"Stage '{name}' depends on '{dep}', which is not enabled")

    def _plan_from_parallel_groups(self, groups: List[List[str]], enabled: List[str]) -> List[List[str]]:
        flattened = [name for group in groups for name in group]
        if len(set(flattened)) != len(flattened):
            raise PipelineError("Duplicate stage in parallel groups")
        if set(flattened) != set(enabled):
            raise PipelineError("Parallel groups must include all enabled stages")

        index_of = {}
        for i, group in enumerate(groups):
            for name in group:
                index_of[name] = i

        for name in enabled:
            for dep in self.stages[name].depends_on:
                if index_of[dep] >= index_of[name]:
                    raise PipelineError(
                        f"Invalid parallel plan: '{name}' depends on '{dep}' in same or later group"
                    )
        return groups

    def _plan_sequential(self, order: Optional[List[str]], enabled: List[str]) -> List[List[str]]:
        if order:
            if len(set(order)) != len(order):
                raise PipelineError("Duplicate stage in order")
            if set(order) != set(enabled):
                raise PipelineError("Order must include all enabled stages")
            ordered = order
        else:
            # Topological-like order based on dependencies
            ordered = []
            remaining = set(enabled)
            while remaining:
                progressed = False
                for name in list(remaining):
                    deps = self.stages[name].depends_on
                    if all(dep in ordered for dep in deps):
                        ordered.append(name)
                        remaining.remove(name)
                        progressed = True
                if not progressed:
                    raise PipelineError("Cyclic dependency detected in stages")
        return [[name] for name in ordered]

    def build_plan(
        self,
        enabled: List[str],
        order: Optional[List[str]] = None,
        parallel_groups: Optional[List[List[str]]] = None,
    ) -> List[List[str]]:
        self._validate_stages(enabled)
        if parallel_groups:
            return self._plan_from_parallel_groups(parallel_groups, enabled)
        return self._plan_sequential(order, enabled)

    def run(
        self,
        context: Dict[str, Any],
        enabled: List[str],
        order: Optional[List[str]] = None,
        parallel_groups: Optional[List[List[str]]] = None,
    ) -> Dict[str, Any]:
        plan = self.build_plan(enabled, order, parallel_groups)
        results: Dict[str, Any] = {}

        for group in plan:
            if len(group) == 1:
                name = group[0]
                results[name] = self.stages[name].run(context, results)
                continue

            with ThreadPoolExecutor(max_workers=len(group)) as executor:
                future_map = {
                    executor.submit(self.stages[name].run, context, results): name
                    for name in group
                }
                for future in future_map:
                    name = future_map[future]
                    results[name] = future.result()

        return results
