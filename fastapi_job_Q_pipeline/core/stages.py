from __future__ import annotations

import time
from typing import Any, Dict

import pandas as pd

from core.interfaces import Stage


class Stage1LoadAndNormalize(Stage):
    name = "stage1"
    depends_on = []

    def run(self, context: Dict[str, Any], results: Dict[str, Any]) -> pd.DataFrame:
        input_path = context["input_path"]
        df = pd.read_excel(input_path)
        if "_row_id" not in df.columns:
            df = df.copy()
            df["_row_id"] = range(1, len(df) + 1)
        time.sleep(0.2)
        return df


class Stage2CpuTransform(Stage):
    name = "stage2"
    depends_on = ["stage1"]

    def run(self, context: Dict[str, Any], results: Dict[str, Any]) -> pd.DataFrame:
        df: pd.DataFrame = results["stage1"]
        df = df.copy()
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            df["_numeric_sum"] = df[numeric_cols].sum(axis=1)
        else:
            df["_numeric_sum"] = 0
        # Simulate CPU work
        total = 0
        for i in range(20000):
            total += i * i
        df["_cpu_marker"] = total % 97
        return df


class Stage3WriteOutput(Stage):
    name = "stage3"
    depends_on = ["stage2"]

    def run(self, context: Dict[str, Any], results: Dict[str, Any]) -> str:
        df: pd.DataFrame = results["stage2"]
        output_path = context["output_path"]
        df.to_csv(output_path, index=False)
        time.sleep(0.2)
        return output_path
