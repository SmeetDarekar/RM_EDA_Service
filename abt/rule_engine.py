def evaluate_single_abt_rules(metrics):
    """
    Deterministic rule engine.
    Returns standardized insights (INFO/WARN/RISK).
    """

    insights = []

    def add(level, category, title, obs, impact, action, evidence=None):
        insights.append({
            "type": level,
            "category": category,
            "title": title,
            "observation": obs,
            "impact": impact,
            "suggestedAction": action,
            "evidence": evidence or {}
        })

    # ----------------------------------
    # ABT health
    # ----------------------------------
    add(
        "INFO",
        "MODEL_READINESS",
        "ABT structure assessed",
        f"ABT contains {metrics['total_columns']} columns "
        f"with {metrics['usable_numeric_columns']} usable numeric features.",
        "Provides a baseline indication of modeling capacity.",
        "Proceed to feature review."
    )

    # ----------------------------------
    # Missingness risk
    # ----------------------------------
    if metrics["high_missing_columns"]:
        add(
            "WARN",
            "DATA_QUALITY",
            "High missingness detected",
            f"{len(metrics['high_missing_columns'])} columns exceed 50% missingness.",
            "Such features may introduce instability or bias.",
            "Consider dropping or imputing these columns.",
            {"columns": metrics["high_missing_columns"]}
        )

    # ----------------------------------
    # Constant features
    # ----------------------------------
    if metrics["constant_columns"]:
        add(
            "WARN",
            "FEATURE_QUALITY",
            "Low-variance features detected",
            f"{len(metrics['constant_columns'])} constant or near-constant features found.",
            "These provide no predictive signal.",
            "Remove these features before modeling.",
            {"columns": metrics["constant_columns"]}
        )

    # ----------------------------------
    # Identifier leakage
    # ----------------------------------
    if metrics["identifier_columns"]:
        add(
            "WARN",
            "GOVERNANCE",
            "Identifier-like features present",
            f"{len(metrics['identifier_columns'])} identifier-like columns detected.",
            "May cause target leakage or governance violations.",
            "Exclude identifiers from feature set.",
            {"columns": metrics["identifier_columns"]}
        )

    # ----------------------------------
    # Target checks
    # ----------------------------------
    if not metrics["target_candidates"]:
        add(
            "RISK",
            "MODEL_READINESS",
            "No target identified",
            "No clear target column detected.",
            "Model training and validation cannot proceed.",
            "Confirm and define the target variable explicitly."
        )

    elif len(metrics["target_candidates"]) > 1:
        add(
            "WARN",
            "MODEL_READINESS",
            "Multiple target candidates",
            f"Multiple target-like columns detected: {metrics['target_candidates']}",
            "Ambiguity may lead to incorrect model training.",
            "Select and lock one target variable.",
            {"targets": metrics["target_candidates"]}
        )

    # ----------------------------------
    # Modeling sufficiency
    # ----------------------------------
    if (
        metrics["numeric_columns"] > 0 and
        metrics["usable_numeric_columns"] < max(2, 0.1 * metrics["numeric_columns"])
    ):
        add(
            "WARN",
            "MODEL_READINESS",
            "Limited modeling signal",
            "Very few usable numeric features detected.",
            "Model performance may be constrained.",
            "Consider feature engineering or enrichment."
        )

    return insights