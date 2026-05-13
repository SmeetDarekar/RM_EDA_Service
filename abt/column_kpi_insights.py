# # abt/column_kpi_insights.py

# def generate_column_kpi_insights(
#     base_snapshot,
#     compare_snapshot=None,
#     max_insights=50
# ):
#     """
#     Generate column-level KPI insights using:
#     Column → KPI → Value(s) → Drift → Interpretation

#     If compare_snapshot is None → single ABT (Analyze)
#     If compare_snapshot provided → delta-based (Compare)
#     """

#     insights = []

#     base_cols = base_snapshot.columns
#     compare_cols = compare_snapshot.columns if compare_snapshot else None

#     for col_name, base_col in base_cols.items():
#         compare_col = compare_cols.get(col_name) if compare_cols else None

#         # ------------------------------
#         # 1. Completeness
#         # ------------------------------
#         base_comp = base_col.completeness_pct
#         compare_comp = compare_col.completeness_pct if compare_col else None

#         if base_comp is not None:
#             drift = (
#                 round(compare_comp - base_comp, 2)
#                 if compare_comp is not None
#                 else None
#             )

#             if base_comp < 80 or (drift is not None and drift < -10):
#                 insights.append({
#                     "column": col_name,
#                     "kpi": "Completeness",
#                     "base_value": base_comp,
#                     "compare_value": compare_comp,
#                     "drift": drift,
#                     "interpretation": "Data availability degraded significantly"
#                 })

#         # ------------------------------
#         # 2. Mean (event rate / center)
#         # ------------------------------
#         base_mean = base_col.mean
#         compare_mean = compare_col.mean if compare_col else None

#         if base_mean is not None:
#             drift = (
#                 round(compare_mean - base_mean, 4)
#                 if compare_mean is not None
#                 else None
#             )

#             if base_col.scale == "binary":
#                 if base_mean < 0.05 or base_mean > 0.95:
#                     insights.append({
#                         "column": col_name,
#                         "kpi": "Mean (event rate)",
#                         "base_value": base_mean,
#                         "compare_value": compare_mean,
#                         "drift": drift,
#                         "interpretation": "Binary target shows severe class imbalance"
#                     })
#                 elif drift is not None and abs(drift) > 0.05:
#                     insights.append({
#                         "column": col_name,
#                         "kpi": "Mean (event rate)",
#                         "base_value": base_mean,
#                         "compare_value": compare_mean,
#                         "drift": drift,
#                         "interpretation": "Target event rate changed materially"
#                     })

#         # ------------------------------
#         # 3. Standard Deviation
#         # ------------------------------
#         base_std = base_col.std
#         compare_std = compare_col.std if compare_col else None

#         if base_std is not None:
#             if base_std == 0:
#                 insights.append({
#                     "column": col_name,
#                     "kpi": "Standard deviation",
#                     "base_value": base_std,
#                     "compare_value": compare_std,
#                     "drift": None,
#                     "interpretation": "Feature provides no predictive signal"
#                 })
#             elif compare_std is not None:
#                 drift = round(compare_std - base_std, 4)
#                 if abs(drift) / base_std > 0.5:
#                     insights.append({
#                         "column": col_name,
#                         "kpi": "Standard deviation",
#                         "base_value": base_std,
#                         "compare_value": compare_std,
#                         "drift": drift,
#                         "interpretation": "Variance changed significantly across versions"
#                     })

#         # ------------------------------
#         # 4. Skewness
#         # ------------------------------
#         if base_col.skewness is not None:
#             if abs(base_col.skewness) > 2:
#                 insights.append({
#                     "column": col_name,
#                     "kpi": "Skewness",
#                     "base_value": base_col.skewness,
#                     "compare_value": None,
#                     "drift": None,
#                     "interpretation": "Distribution is highly skewed"
#                 })

#         # ------------------------------
#         # 5. Cardinality
#         # ------------------------------
#         if base_col.cardinality is not None:
#             if base_col.cardinality <= 2 and base_col.scale not in ("binary",):
#                 insights.append({
#                     "column": col_name,
#                     "kpi": "Cardinality",
#                     "base_value": base_col.cardinality,
#                     "compare_value": None,
#                     "drift": None,
#                     "interpretation": "Low feature variability limits predictive value"
#                 })

#         # ------------------------------
#         # 6. Uniqueness (leakage risk)
#         # ------------------------------
#         if base_col.has_unique:
#             insights.append({
#                 "column": col_name,
#                 "kpi": "Uniqueness",
#                 "base_value": "High",
#                 "compare_value": None,
#                 "drift": None,
#                 "interpretation": "Identifier-like behavior may cause leakage"
#             })

#         if len(insights) >= max_insights:
#             break

#     return insights








# abt/column_kpi_insights.py

# def generate_column_kpi_insights(
#     base_snapshot,
#     compare_snapshot=None,
#     max_insights=200
# ):
#     """ 
#     Generate column-level KPI insights using:
#     Column → KPI → Value(s) → Drift → Interpretation

#     This version EXTENDS KPI coverage without
#     changing any existing filtering logic.
#     """

#     insights = []

#     base_cols = base_snapshot.columns
#     compare_cols = compare_snapshot.columns if compare_snapshot else None

#     for col_name, base_col in base_cols.items():
#         compare_col = compare_cols.get(col_name) if compare_cols else None

#         # ------------------------------
#         # 1. Completeness
#         # ------------------------------
#         base_comp = base_col.completeness_pct
#         compare_comp = compare_col.completeness_pct if compare_col else None

#         drift = (
#             round(compare_comp - base_comp, 2)
#             if base_comp is not None and compare_comp is not None
#             else None
#         )

#         insights.append({
#             "column": col_name,
#             "kpi": "Completeness",
#             "base_value": base_comp,
#             "compare_value": compare_comp,
#             "drift": drift,
#             "interpretation": "Data availability measure"
#         })

#         # ------------------------------
#         # 2. Mean
#         # ------------------------------
#         base_mean = base_col.mean
#         compare_mean = compare_col.mean if compare_col else None

#         drift = (
#             round(compare_mean - base_mean, 6)
#             if base_mean is not None and compare_mean is not None
#             else None
#         )

#         insights.append({
#             "column": col_name,
#             "kpi": "Mean",
#             "base_value": base_mean,
#             "compare_value": compare_mean,
#             "drift": drift,
#             "interpretation": "Average value of the distribution"
#         })

#         # ------------------------------
#         # 3. Median
#         # ------------------------------
#         insights.append({
#             "column": col_name,
#             "kpi": "Median",
#             "base_value": base_col.median,
#             "compare_value": compare_col.median if compare_col else None,
#             "drift": None,
#             "interpretation": "Robust central tendency indicator"
#         })

#         # ------------------------------
#         # 4. Standard Deviation
#         # ------------------------------
#         base_std = base_col.std
#         compare_std = compare_col.std if compare_col else None

#         drift = (
#             round(compare_std - base_std, 6)
#             if base_std is not None and compare_std is not None
#             else None
#         )

#         insights.append({
#             "column": col_name,
#             "kpi": "Standard Deviation",
#             "base_value": base_std,
#             "compare_value": compare_std,
#             "drift": drift,
#             "interpretation": "Spread and signal strength indicator"
#         })

#         # ------------------------------
#         # 5. Skewness
#         # ------------------------------
#         insights.append({
#             "column": col_name,
#             "kpi": "Skewness",
#             "base_value": base_col.skewness,
#             "compare_value": compare_col.skewness if compare_col else None,
#             "drift": None,
#             "interpretation": "Distribution asymmetry indicator"
#         })

#         # ------------------------------
#         # 6. Kurtosis
#         # ------------------------------
#         insights.append({
#             "column": col_name,
#             "kpi": "Kurtosis",
#             "base_value": base_col.kurtosis,
#             "compare_value": compare_col.kurtosis if compare_col else None,
#             "drift": None,
#             "interpretation": "Tail heaviness indicator"
#         })

#         # ------------------------------
#         # 7. Cardinality
#         # ------------------------------
#         insights.append({
#             "column": col_name,
#             "kpi": "Cardinality",
#             "base_value": base_col.cardinality,
#             "compare_value": compare_col.cardinality if compare_col else None,
#             "drift": None,
#             "interpretation": "Distinct value count"
#         })

#         # ------------------------------
#         # 8. Uniqueness
#         # ------------------------------
#         insights.append({
#             "column": col_name,
#             "kpi": "Uniqueness",
#             "base_value": base_col.has_unique,
#             "compare_value": compare_col.has_unique if compare_col else None,
#             "drift": None,
#             "interpretation": "Identifier-like behavior flag"
#         })

#         # ------------------------------
#         # 9. Outliers
#         # ------------------------------
#         insights.append({
#             "column": col_name,
#             "kpi": "Outliers",
#             "base_value": base_col.n_outliers if hasattr(base_col, "n_outliers") else None,
#             "compare_value": (
#                 compare_col.n_outliers if compare_col and hasattr(compare_col, "n_outliers") else None
#             ),
#             "drift": None,
#             "interpretation": "Extreme value presence indicator"
#         })

#         if len(insights) >= max_insights:
#             break

#     return insights





























# abt/column_kpi_insights.py

# SEVERITY_RANK = {
#     "Governance": 1,
#     "No Signal": 2,
#     "Low Variability": 3,
#     "Data Availability": 4,
#     "Distribution Shape": 5,
# }


# def generate_analyze_column_kpi_insights(abt_snapshot, max_rows=200):
#     """
#     Analyze-only KPI → Insight generator.

#     Final output format:
#     Column → KPI → Value → Interpretation

#     No drift.
#     No comparison.
#     """

#     raw_insights = []

#     for col_name, col in abt_snapshot.columns.items():

#         # ------------------------------
#         # A. Data Availability
#         # ------------------------------
#         if col.completeness_pct is not None and col.completeness_pct < 100:
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Completeness",
#                 "value": col.completeness_pct,
#                 "category": "Data Availability",
#                 "interpretation": (
#                     f"Completeness {col.completeness_pct}% indicates missing data"
#                 )
#             })

#         # ------------------------------
#         # B. No Predictive Signal
#         # ------------------------------
#         if col.std == 0:
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Standard Deviation",
#                 "value": col.std,
#                 "category": "No Signal",
#                 "interpretation": "Standard deviation is zero; column provides no predictive signal"
#             })

#         if col.scale == "unary":
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Statistical Scale",
#                 "value": col.scale,
#                 "category": "No Signal",
#                 "interpretation": "Unary scale indicates constant-valued feature"
#             })

#         # ------------------------------
#         # C. Low Variability
#         # ------------------------------
#         if col.cardinality is not None and col.cardinality <= 2 and col.scale != "binary":
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Cardinality",
#                 "value": col.cardinality,
#                 "category": "Low Variability",
#                 "interpretation": f"Cardinality {col.cardinality} suggests very limited variability"
#             })

#         # ------------------------------
#         # D. Distribution Shape (informational)
#         # ------------------------------
#         if col.skewness is not None:
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Skewness",
#                 "value": col.skewness,
#                 "category": "Distribution Shape",
#                 "interpretation": f"Skewness {round(col.skewness, 3)} indicates asymmetric distribution"
#             })

#         if col.kurtosis is not None:
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Kurtosis",
#                 "value": col.kurtosis,
#                 "category": "Distribution Shape",
#                 "interpretation": f"Kurtosis {round(col.kurtosis, 3)} indicates heavy-tailed behavior"
#             })

#         # ------------------------------
#         # E. Governance
#         # ------------------------------
#         if col.has_unique:
#             raw_insights.append({
#                 "column": col_name,
#                 "kpi": "Uniqueness",
#                 "value": "High",
#                 "category": "Governance",
#                 "interpretation": "Identifier-like behavior detected (high uniqueness)"
#             })

#         if len(raw_insights) >= max_rows:
#             break

#     return raw_insights


# def filter_analyze_column_kpi_insights(raw_insights):
#     """
#     Analyze-only relevance filtering.
#     Removes noise and sorts by severity.
#     """

#     filtered = []
#     primary_issue_columns = set()

#     # First pass: identify columns with real issues
#     for row in raw_insights:
#         if row["category"] in (
#             "Governance",
#             "No Signal",
#             "Low Variability",
#             "Data Availability"
#         ):
#             primary_issue_columns.add(row["column"])

#     # Second pass: filter
#     for row in raw_insights:
#         if row["category"] == "Distribution Shape":
#             if row["column"] not in primary_issue_columns:
#                 continue  # suppress pure shape-only noise

#         filtered.append(row)

#     # Sort deterministically
#     filtered.sort(
#         key=lambda r: (
#             SEVERITY_RANK.get(r["category"], 99),
#             r["column"],
#             r["kpi"]
#         )
#     )

#     return filtered







# abt/column_kpi_insights.py

SEVERITY_RANK = {
    "Governance": 1,
    "No Signal": 2,
    "Low Variability": 3,
    "Data Availability": 4,
    "Distribution Shape": 5,
}


# ==========================================================
# ANALYZE: intrinsic column issues
# ==========================================================
def generate_analyze_column_kpi_insights(abt_snapshot, max_rows=200):
    raw = []

    for col_name, col in abt_snapshot.columns.items():

        # Data availability
        if col.completeness_pct is not None and col.completeness_pct < 100:
            raw.append({
                "column": col_name,
                "kpi": "Completeness",
                "base_value": col.completeness_pct,
                "compare_value": None,
                "category": "Data Availability",
                "interpretation": f"Completeness {col.completeness_pct}% indicates missing data"
            })

        # No signal
        if col.std == 0 or col.scale == "unary":
            raw.append({
                "column": col_name,
                "kpi": "Variance",
                "base_value": col.std,
                "compare_value": None,
                "category": "No Signal",
                "interpretation": "Column provides no predictive signal"
            })

        # Low variability
        if col.cardinality is not None and col.cardinality <= 2 and col.scale != "binary":
            raw.append({
                "column": col_name,
                "kpi": "Cardinality",
                "base_value": col.cardinality,
                "compare_value": None,
                "category": "Low Variability",
                "interpretation": f"Only {col.cardinality} distinct values observed"
            })

        # Shape (informational)
        if col.skewness is not None:
            raw.append({
                "column": col_name,
                "kpi": "Skewness",
                "base_value": col.skewness,
                "compare_value": None,
                "category": "Distribution Shape",
                "interpretation": f"Skewness {round(col.skewness,3)} indicates asymmetric distribution"
            })

        if col.kurtosis is not None:
            raw.append({
                "column": col_name,
                "kpi": "Kurtosis",
                "base_value": col.kurtosis,
                "compare_value": None,
                "category": "Distribution Shape",
                "interpretation": f"Kurtosis {round(col.kurtosis,3)} indicates heavy-tailed behavior"
            })

        # Governance
        if col.has_unique:
            raw.append({
                "column": col_name,
                "kpi": "Uniqueness",
                "base_value": "High",
                "compare_value": None,
                "category": "Governance",
                "interpretation": "Identifier-like behavior detected"
            })

        if len(raw) >= max_rows:
            break

    return raw


def filter_analyze_column_kpi_insights(raw):
    keep = []
    problem_cols = set()

    for r in raw:
        if r["category"] != "Distribution Shape":
            problem_cols.add(r["column"])

    for r in raw:
        if r["category"] == "Distribution Shape" and r["column"] not in problem_cols:
            continue
        keep.append(r)

    keep.sort(
        key=lambda r: (
            SEVERITY_RANK.get(r["category"], 99),
            r["column"],
            r["kpi"]
        )
    )

    return keep


# ==========================================================
# COMPARE: delta-based insights only
# ==========================================================
def generate_compare_column_kpi_insights(base_snapshot, compare_snapshot, max_rows=200):
    insights = []

    base_cols = base_snapshot.columns
    comp_cols = compare_snapshot.columns

    all_cols = set(base_cols) | set(comp_cols)

    for col in all_cols:
        b = base_cols.get(col)
        c = comp_cols.get(col)

        # Column removed
        if b and not c:
            insights.append({
                "column": col,
                "kpi": "Presence",
                "base_value": "Present",
                "compare_value": "Removed",
                "category": "Governance",
                "interpretation": "Column removed in new ABT version"
            })
            continue

        # New column
        if c and not b:
            insights.append({
                "column": col,
                "kpi": "Presence",
                "base_value": "Absent",
                "compare_value": "Added",
                "category": "Governance",
                "interpretation": "New column introduced in new ABT version"
            })
            continue

        # KPI deltas only
        for kpi_name, attr in [
            ("Completeness", "completeness_pct"),
            ("Standard Deviation", "std"),
            ("Cardinality", "cardinality"),
            ("Skewness", "skewness"),
            ("Kurtosis", "kurtosis"),
        ]:
            bval = getattr(b, attr)
            cval = getattr(c, attr)

            if bval is None or cval is None:
                continue

            if bval != cval:
                insights.append({
                    "column": col,
                    "kpi": kpi_name,
                    "base_value": bval,
                    "compare_value": cval,
                    "category": "Data Change",
                    "interpretation": f"{kpi_name} changed across ABT versions"
                })

        # Governance delta
        if b.has_unique != c.has_unique:
            insights.append({
                "column": col,
                "kpi": "Uniqueness",
                "base_value": b.has_unique,
                "compare_value": c.has_unique,
                "category": "Governance",
                "interpretation": "Identifier-like behavior changed across versions"
            })

        if len(insights) >= max_rows:
            break

    return insights