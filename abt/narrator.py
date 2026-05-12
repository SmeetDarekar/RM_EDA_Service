# abt/narrator.py

def narrate_insight(
    *,
    column_name: str,
    category: str,
    severity: str,
    stage_span: str,
    observed_behavior: list[str],
    pattern: str,
    likely_cause: str,
    risk_implication: list[str],
    recommended_action: str,
    evidence: dict
):
    """
    Builds an evidence-first, risk-grade insight explanation.
    """

    return {
        "severity": severity,
        "category": category,
        "column": column_name,
        "stage": stage_span,

        "observed_behavior": observed_behavior,
        "detected_pattern": pattern,
        "likely_cause": likely_cause,
        "risk_implication": risk_implication,
        "recommended_action": recommended_action,

        "evidence": evidence
    }