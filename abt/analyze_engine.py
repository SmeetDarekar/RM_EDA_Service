# abt/analyze_engine.py

def generate_single_abt_insights(abt):
    """
    Simple, business‑meaningful single‑ABT analysis.

    Returns a LIST of insights compatible with existing UI.
    """

    insights = []

    total_columns = len(abt.columns)

    high_missing = []
    constant_cols = []
    identifier_cols = []
    target_cols = []

    numeric_columns = 0
    usable_numeric_columns = 0

    for col_name, col in abt.columns.items():

        # ------------------------------
        # Missingness
        # ------------------------------
        if col.missing_pct is not None and col.missing_pct >= 50:
            high_missing.append(col_name)

        # ------------------------------
        # Constant / near‑constant
        # ------------------------------
        if col.is_constant_like():
            constant_cols.append(col_name)
            continue

        # ------------------------------
        # Identifier‑like
        # ------------------------------
        if col.is_identifier_like():
            identifier_cols.append(col_name)

        # ------------------------------
        # Target candidates
        # ------------------------------
        if col.is_target_candidate():
            target_cols.append(col_name)

        # ------------------------------
        # Numeric usability
        # ------------------------------
        if col.has_variance():
            numeric_columns += 1
            if not col.is_constant_like() and not col.is_identifier_like():
                usable_numeric_columns += 1

    # ==================================================
    # ABT‑LEVEL INTERPRETIVE INSIGHTS
    # ==================================================

    # Helper to format column list cleanly
    def format_cols(cols, max_cols=5):
        if not cols:
            return ""
        shown = cols[:max_cols]
        suffix = "..." if len(cols) > max_cols else ""
        return ", ".join(shown) + suffix

    # 1. Overall ABT health
    insights.append({
        "category": "ABT_HEALTH",
        "severity": "INFO",
        "column": None,
        "message": (
            f"ABT contains {total_columns} columns, of which "
            f"{usable_numeric_columns} are usable numeric features."
        ),
        "evidence": {}
    })

    # 2. High missingness
    if high_missing:
        insights.append({
            "category": "DATA_QUALITY",
            "severity": "WARN",
            "column": None,
            "message": (
                f"{len(high_missing)} columns have more than 50% missing values. "
                "Such features provide limited signal and may degrade model stability. "
                f"Affected columns: {format_cols(high_missing)}"
            ),
            "evidence": {
                "affected_columns": high_missing
            }
        })

    # 3. Constant features
    if constant_cols:
        insights.append({
            "category": "FEATURE_QUALITY",
            "severity": "WARN",
            "column": None,
            "message": (
                f"{len(constant_cols)} columns show very low or zero variance. "
                "These features do not contribute predictive value and can be safely removed. "
                f"Affected columns: {format_cols(constant_cols)}"
            ),
            "evidence": {
                "affected_columns": constant_cols
            }
        })

    # 4. Identifier leakage risk
    if identifier_cols:
        insights.append({
            "category": "GOVERNANCE",
            "severity": "WARN",
            "column": None,
            "message": (
                f"{len(identifier_cols)} identifier‑like columns were detected. "
                "Including such fields may cause target leakage or governance issues. "
                f"Affected columns: {format_cols(identifier_cols)}"
            ),
            "evidence": {
                "affected_columns": identifier_cols
            }
        })

    # 5. Target clarity
    if not target_cols:
        insights.append({
            "category": "TARGET_CHECK",
            "severity": "CRITICAL",
            "column": None,
            "message": (
                "No clear target column was detected in the ABT. "
                "Model training and validation cannot proceed until the target is confirmed."
            ),
            "evidence": {}
        })

    elif len(target_cols) > 1:
        insights.append({
            "category": "TARGET_CHECK",
            "severity": "WARN",
            "column": None,
            "message": (
                "Multiple potential target‑like columns were detected. "
                "This may lead to ambiguity during model training. "
                f"Candidates: {format_cols(target_cols)}"
            ),
            "evidence": {
                "affected_columns": target_cols
            }
        })

    # 6. Low modeling readiness
    if numeric_columns > 0 and usable_numeric_columns < max(2, 0.1 * numeric_columns):
        insights.append({
            "category": "MODEL_READINESS",
            "severity": "WARN",
            "column": None,
            "message": (
                "Only a small subset of numeric features appear usable for modeling. "
                "This may limit model performance and robustness."
            ),
            "evidence": {
                "numeric_columns": numeric_columns,
                "usable_numeric_columns": usable_numeric_columns
            }
        })

    return insights
























# abt/analyze_engine.py

# def generate_single_abt_insights(abt):
#     """
#     Simple, business‑meaningful single‑ABT analysis.

#     Returns a LIST of insights compatible with existing UI.
#     Each insight explains:
#     - what is observed
#     - why it matters
#     - how it may affect downstream modeling
#     """

#     insights = []

#     total_columns = len(abt.columns)

#     high_missing = []
#     constant_cols = []
#     identifier_cols = []
#     target_cols = []

#     numeric_columns = 0
#     usable_numeric_columns = 0

#     for col_name, col in abt.columns.items():

#         # ------------------------------
#         # Missingness
#         # ------------------------------
#         if col.missing_pct is not None and col.missing_pct >= 50:
#             high_missing.append(col_name)

#         # ------------------------------
#         # Constant / near‑constant
#         # ------------------------------
#         if col.is_constant_like():
#             constant_cols.append(col_name)
#             continue

#         # ------------------------------
#         # Identifier‑like
#         # ------------------------------
#         if col.is_identifier_like():
#             identifier_cols.append(col_name)

#         # ------------------------------
#         # Target candidates
#         # ------------------------------
#         if col.is_target_candidate():
#             target_cols.append(col_name)

#         # ------------------------------
#         # Numeric usability
#         # ------------------------------
#         if col.has_variance():
#             numeric_columns += 1
#             if not col.is_constant_like() and not col.is_identifier_like():
#                 usable_numeric_columns += 1

#     # ==================================================
#     # ABT‑LEVEL INTERPRETIVE INSIGHTS
#     # ==================================================

#     # 1. Overall ABT health
#     insights.append({
#         "category": "ABT_HEALTH",
#         "severity": "INFO",
#         "column": None,
#         "message": (
#             f"ABT contains {total_columns} columns, "
#             f"of which {usable_numeric_columns} are usable numeric features."
#         ),
#         "evidence": {
#             "total_columns": total_columns,
#             "usable_numeric_columns": usable_numeric_columns
#         }
#     })

#     # 2. High missingness
#     if high_missing:
#         insights.append({
#             "category": "DATA_QUALITY",
#             "severity": "WARN",
#             "column": None,
#             "message": (
#                 f"{len(high_missing)} columns have more than 50% missing values. "
#                 "Such features provide limited signal and may degrade model stability "
#                 "if heavily imputed."
#             ),
#             "evidence": {
#                 "affected_columns": high_missing[:10]
#             }
#         })

#     # 3. Constant features
#     if constant_cols:
#         insights.append({
#             "category": "FEATURE_QUALITY",
#             "severity": "WARN",
#             "column": None,
#             "message": (
#                 f"{len(constant_cols)} columns show very low or zero variance. "
#                 "These features do not contribute predictive value and can be safely removed "
#                 "before model training."
#             ),
#             "evidence": {
#                 "affected_columns": constant_cols[:10]
#             }
#         })

#     # 4. Identifier leakage risk
#     if identifier_cols:
#         insights.append({
#             "category": "GOVERNANCE",
#             "severity": "WARN",
#             "column": None,
#             "message": (
#                 f"{len(identifier_cols)} identifier‑like columns were detected. "
#                 "Including such fields in modeling may cause target leakage or "
#                 "governance issues."
#             ),
#             "evidence": {
#                 "affected_columns": identifier_cols[:10]
#             }
#         })

#     # 5. Target clarity
#     if not target_cols:
#         insights.append({
#             "category": "TARGET_CHECK",
#             "severity": "CRITICAL",
#             "column": None,
#             "message": (
#                 "No clear target column was detected in the ABT. "
#                 "Model training and validation cannot proceed until "
#                 "the target definition is confirmed."
#             ),
#             "evidence": {}
#         })

#     elif len(target_cols) > 1:
#         insights.append({
#             "category": "TARGET_CHECK",
#             "severity": "WARN",
#             "column": None,
#             "message": (
#                 "Multiple potential target‑like columns were detected. "
#                 "Ambiguous target definitions may lead to inconsistent "
#                 "model results."
#             ),
#             "evidence": {
#                 "affected_columns": target_cols
#             }
#         })

#     # 6. Low modeling readiness
#     if numeric_columns > 0 and usable_numeric_columns < max(2, 0.1 * numeric_columns):
#         insights.append({
#             "category": "MODEL_READINESS",
#             "severity": "WARN",
#             "column": None,
#             "message": (
#                 "Only a small subset of numeric features appear usable for modeling. "
#                 "This may limit model quality and robustness."
#             ),
#             "evidence": {
#                 "numeric_columns": numeric_columns,
#                 "usable_numeric_columns": usable_numeric_columns
#             }
#         })

#     return insights