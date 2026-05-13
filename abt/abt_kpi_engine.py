def compute_abt_level_kpis(abt_base, abt_compare, target_column=None):
    """
    Compute ABT-level KPIs for comparison.
    Implements Rules 2.2-A, 2.2-B, 2.2-C without breaking existing logic.
    """

    base_cols = abt_base.columns
    comp_cols = abt_compare.columns

    base_col_names = set(base_cols.keys())
    comp_col_names = set(comp_cols.keys())

    # ---------------------------
    # Structural KPIs
    # ---------------------------
    # Rule 2.2-A: Base ⊆ Compare (mandatory)
    missing_columns = sorted(base_col_names - comp_col_names)

    # Rule 2.2-B: Additional columns allowed
    additional_columns = sorted(comp_col_names - base_col_names)

    # ---------------------------
    # Missingness KPI (median)
    # ---------------------------
    def median(values):
        v = sorted(values)
        n = len(v)
        if n == 0:
            return None
        return v[n // 2] if n % 2 else (v[n//2 - 1] + v[n//2]) / 2

    base_missing = [
        c.missing_pct for c in base_cols.values()
        if c.missing_pct is not None
    ]
    comp_missing = [
        c.missing_pct for c in comp_cols.values()
        if c.missing_pct is not None
    ]

    base_missing_median = median(base_missing)
    comp_missing_median = median(comp_missing)

    missing_delta = (
        comp_missing_median - base_missing_median
        if base_missing_median is not None and comp_missing_median is not None
        else None
    )

    # ---------------------------
    # Mean stability KPI
    # ---------------------------
    mean_within_tol = 0
    mean_total = 0
    red_flag_columns = []

    for col in base_col_names & comp_col_names:
        b = base_cols[col]
        c = comp_cols[col]

        if b.mean is not None and c.mean is not None:
            mean_total += 1
            if abs(c.mean - b.mean) <= 0.1:
                mean_within_tol += 1
            else:
                red_flag_columns.append(col)

    mean_alignment_pct = (
        round((mean_within_tol / mean_total) * 100, 2)
        if mean_total > 0 else None
    )

    # ---------------------------
    # Verdict Rules (v2 – structured)
    # ---------------------------
    verdict = "ACCEPTED"
    reasons = []

    # Rule 2.2-A: Structural backward compatibility
    if missing_columns:
        verdict = "REJECTED"
        reasons.append("Base columns missing in compare ABT")

    # Rule 2.2-C: Target column must persist
    if target_column:
        if target_column not in comp_col_names:
            verdict = "REJECTED"
            reasons.append(f"Target column '{target_column}' missing in compare ABT")

    # Existing data quality rule (unchanged)
    if missing_delta is not None and missing_delta > 0.5:
        verdict = "REJECTED"
        reasons.append("Significant increase in missingness")

    # Existing statistical stability rule (unchanged)
    if mean_alignment_pct is not None and mean_alignment_pct < 75:
        verdict = "REJECTED"
        reasons.append("Large statistical deviation in features")

    if not reasons:
        reasons.append("Within acceptable limits")

    # ---------------------------
    # Final Output
    # ---------------------------
    return {
        "structural": {
            "missing_columns_count": len(missing_columns),
            "additional_columns_count": len(additional_columns),
            "missing_columns": missing_columns,
            "additional_columns": additional_columns,
        },
        "data_quality": {
            "base_missing_median": base_missing_median,
            "compare_missing_median": comp_missing_median,
            "missing_delta": missing_delta,
        },
        "statistical_alignment": {
            "mean_alignment_pct": mean_alignment_pct,
            "red_flag_columns": red_flag_columns[:10],
            "total_compared": mean_total,
        },
        "verdict": {
            "result": verdict,
            "reasons": reasons,
        }
    }