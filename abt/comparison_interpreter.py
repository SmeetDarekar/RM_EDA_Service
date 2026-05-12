# abt/comparison_interpreter.py

def interpret_comparison(kpis):
    """
    Interpret ABT comparison KPIs into decision-grade insights.
    No new metrics. No statistics. Pure reasoning.
    """

    insights = []

    structural = kpis["structural"]
    stats = kpis["statistical_alignment"]
    verdict = kpis["verdict"]

    missing_cols = structural["missing_columns"]
    additional_cols = structural["additional_columns"]
    total_compared = stats["total_compared"]

    # --------------------------------------------------
    # 1. STAGE MISMATCH / NOT COMPARABLE
    # --------------------------------------------------
    critical_lineage = {
        "ACTUAL_OUTCOME_VALUE",
        "MODEL_RK",
        "SCORE_TIME_SK"
    }

    missing_critical = critical_lineage & set(missing_cols)

    if missing_critical:
        insights.append({
            "type": "RISK",
            "category": "STRUCTURE",
            "title": "ABT versions are not structurally comparable",
            "observation": (
                "Key outcome or lineage columns are present in the base ABT "
                "but missing in the compared ABT."
            ),
            "evidence": f"Missing critical columns: {sorted(missing_critical)}",
            "impact": (
                "The two datasets represent different lifecycle stages rather than "
                "iterative versions of the same ABT."
            ),
            "suggestedAction": (
                "Compare ABTs from the same pipeline stage (e.g. training vs training), "
                "or document this as an intentional structural transformation."
            )
        })

        insights.append({
            "type": "INFO",
            "category": "MODEL_READINESS",
            "title": "Comparison rejection is structural, not data quality related",
            "observation": (
                "The comparison was rejected due to schema incompatibility, "
                "not due to degraded data quality or instability."
            ),
            "evidence": "Insufficient common features for statistical comparison",
            "impact": (
                "This does not indicate model degradation or poor data health."
            ),
            "suggestedAction": (
                "Treat this comparison as a lineage review rather than a stability check."
            )
        })

        return insights  # ✅ STOP EARLY — nothing else matters

    # --------------------------------------------------
    # 2. GENUINE DATA QUALITY DEGRADATION
    # --------------------------------------------------
    if verdict["result"] == "REJECTED" and "Significant increase in missingness" in verdict["reasons"]:
        insights.append({
            "type": "RISK",
            "category": "DATA_QUALITY",
            "title": "Data quality degradation detected",
            "observation": "Missingness has increased materially in the compared ABT.",
            "evidence": kpis["data_quality"],
            "impact": "Model stability and validation metrics may be unreliable.",
            "suggestedAction": "Investigate upstream data preparation and filtering logic."
        })

    # --------------------------------------------------
    # 3. STATISTICAL DRIFT (VALID COMPARISON)
    # --------------------------------------------------
    if verdict["result"] == "REJECTED" and "Large statistical deviation in features" in verdict["reasons"]:
        insights.append({
            "type": "WARN",
            "category": "FEATURE_QUALITY",
            "title": "Feature distribution drift detected",
            "observation": "Multiple features show significant mean deviation.",
            "evidence": f"{stats['mean_alignment_pct']}% features aligned",
            "impact": "Model recalibration or retraining may be required.",
            "suggestedAction": "Review drifted features and assess retraining need."
        })

    # --------------------------------------------------
    # 4. ACCEPTABLE COMPARISON
    # --------------------------------------------------
    if verdict["result"] == "ACCEPTED":
        insights.append({
            "type": "INFO",
            "category": "MODEL_READINESS",
            "title": "ABT versions are comparable",
            "observation": "No material structural or statistical deviations detected.",
            "evidence": verdict["reasons"],
            "impact": "Model validation and approval can proceed.",
            "suggestedAction": "Proceed with downstream modeling or validation."
        })

    return insights
