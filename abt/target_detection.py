# abt/target_detection.py

from typing import List, Dict


def detect_target_column_from_dump(raw_items: List[Dict]) -> Dict:
    """
    Heuristically detect target column candidates from ABT metadata dump.

    Rules:
    1. Column name contains 'target' (case-insensitive)
    2. Column name starts with 'p_'
    """

    all_columns = []
    target_candidates = []

    for item in raw_items:
        col_name = item.get("name")
        if not col_name:
            continue

        all_columns.append(col_name)

        lname = col_name.lower()
        if "target" in lname or lname.startswith("p_"):
            target_candidates.append(col_name)

    # -------------------------------
    # Decision logic
    # -------------------------------
    if len(target_candidates) == 1:
        return {
            "status": "FOUND",
            "target": target_candidates[0],
            "reason": "Single target candidate detected by heuristic",
            "candidates": target_candidates,
            "all_columns": all_columns
        }

    if len(target_candidates) > 1:
        return {
            "status": "AMBIGUOUS",
            "target": None,
            "reason": "Multiple target-like columns detected",
            "candidates": target_candidates,
            "all_columns": all_columns
        }

    return {
        "status": "NOT_FOUND",
        "target": None,
        "reason": "No target-like column detected using heuristics",
        "candidates": [],
        "all_columns": all_columns
    }