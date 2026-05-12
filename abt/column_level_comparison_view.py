# # abt/column_level_comparison_view.py

# def build_column_level_comparison(
#     base_snapshot,
#     compare_snapshot,
#     max_rows=10
# ):
#     """
#     Column-level comparison using IC-authoritative completenessPercent.
#     This is a PURE ADD-ON and does not affect existing logic.
#     """

#     rows = []

#     base_cols = base_snapshot.columns
#     compare_cols = compare_snapshot.columns

#     common_columns = set(base_cols.keys()) & set(compare_cols.keys())

#     for col in common_columns:
#         base_attr = base_cols[col].attributes
#         comp_attr = compare_cols[col].attributes

#         # ✅ Authoritative completeness from IC metadata
#         base_comp = base_attr.get("completenessPercent")
#         compare_comp = comp_attr.get("completenessPercent")

#         if base_comp is None or compare_comp is None:
#             continue

#         delta = compare_comp - base_comp

#         # ✅ Simple, explainable status rules
#         if delta >= -2:
#             status = "✅ Stable"
#             reason = "Completeness remains stable across ABTs"
#             priority = 3
#         elif delta > -10:
#             status = "⚠️ Degraded"
#             reason = "Moderate completeness degradation observed"
#             priority = 2
#         else:
#             status = "❌ Risky"
#             reason = "Significant completeness drop below acceptable threshold"
#             priority = 1

#         rows.append({
#             "column": col,
#             "base": f"{round(base_comp, 2)}%",
#             "compare": f"{round(compare_comp, 2)}%",
#             "status": status,
#             "priority": priority,
#             "reason": reason
#         })

#     # ✅ Show worst columns first
#     rows.sort(key=lambda x: x["priority"])

#     return rows[:max_rows]







# abt/column_level_comparison_view.py

def build_column_level_comparison(
    base_snapshot,
    compare_snapshot,
    max_rows=10
):
    """
    Column-level comparison using normalized ColumnProfile fields.
    PURE ADD-ON. No recomputation. No raw IC JSON access.
    """

    rows = []

    base_cols = base_snapshot.columns
    compare_cols = compare_snapshot.columns

    common_columns = set(base_cols.keys()) & set(compare_cols.keys())

    for col in common_columns:
        base_col = base_cols[col]
        compare_col = compare_cols[col]

        # ✅ Authoritative, normalized completeness
        base_comp = base_col.completeness_pct
        compare_comp = compare_col.completeness_pct

        if base_comp is None or compare_comp is None:
            continue

        delta = compare_comp - base_comp

        if delta >= -2:
            status = "✅ Stable"
            reason = "Completeness remains stable across ABTs"
            priority = 3
        elif delta > -10:
            status = "⚠️ Degraded"
            reason = "Moderate completeness degradation observed"
            priority = 2
        else:
            status = "❌ Risky"
            reason = "Significant completeness drop below acceptable threshold"
            priority = 1

        rows.append({
            "column": col,
            "base": f"{round(base_comp, 2)}%",
            "compare": f"{round(compare_comp, 2)}%",
            "status": status,
            "priority": priority,
            "reason": reason
        })

    # Worst first
    rows.sort(key=lambda x: x["priority"])

    return rows[:max_rows]