# abt/compare_kpi_addon.py

def build_kpi_comparison_summary(missing_columns, kpis):
    """
    Build KPI-level Accepted / Rejected / Skipped summary
    using existing comparison outputs.
    """

    summary = []

    # --------------------------------------------------
    # Structural Integrity
    # --------------------------------------------------
    summary.append({
        "kpi": "Structural Integrity",
        "base": "All required columns present",
        "compare": f"{len(missing_columns)} columns missing",
        "decision": "REJECTED" if missing_columns else "ACCEPTED",
        "reason": (
            "Missing columns detected"
            if missing_columns
            else "Schemas aligned"
        )
    })

    # --------------------------------------------------
    # Data Completeness
    # --------------------------------------------------
    dq = kpis.get("data_quality", {})
    base_missing = dq.get("base_missing_median")
    compare_missing = dq.get("compare_missing_median")

    if base_missing is None or compare_missing is None:
        summary.append({
            "kpi": "Data Completeness",
            "base": "N/A",
            "compare": "N/A",
            "decision": "SKIPPED",
            "reason": "Insufficient common columns for completeness comparison"
        })
    else:
        summary.append({
            "kpi": "Data Completeness",
            "base": f"{base_missing}%",
            "compare": f"{compare_missing}%",
            "decision": "ACCEPTED",
            "reason": "No significant degradation detected"
        })

    # --------------------------------------------------
    # Statistical Stability
    # --------------------------------------------------
    stat = kpis.get("statistical_alignment", {})
    if stat.get("total_compared", 0) == 0:
        summary.append({
            "kpi": "Statistical Stability",
            "base": "-",
            "compare": "-",
            "decision": "SKIPPED",
            "reason": "Insufficient common numeric features"
        })

    return summary


def build_column_level_quality(base_snapshot, compare_snapshot, max_rows=10):
    """
    Column-level Accepted / Rejected view derived from
    existing ABTSnapshot column metadata.
    """

    rows = []

    base_cols = base_snapshot.columns
    compare_cols = compare_snapshot.columns

    common_cols = set(base_cols.keys()) & set(compare_cols.keys())

    for col in common_cols:
        base_missing = base_cols[col].missing_pct
        compare_missing = compare_cols[col].missing_pct

        if base_missing is None or compare_missing is None:
            continue

        base_comp = round(100 - base_missing, 2)
        compare_comp = round(100 - compare_missing, 2)

        if compare_comp >= base_comp - 5:
            status = "ACCEPTED"
            reason = "Stable completeness"
        else:
            status = "REJECTED"
            reason = "Significant completeness drop"

        rows.append({
            "column": col,
            "base": f"{base_comp}%",
            "compare": f"{compare_comp}%",
            "status": status,
            "reason": reason
        })

    # Rejected first, then accepted
    rows.sort(key=lambda x: x["status"] != "REJECTED")

    return rows[:max_rows]