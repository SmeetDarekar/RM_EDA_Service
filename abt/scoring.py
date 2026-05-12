# abt/scoring.py

def feature_risk_weight(column):
    """
    Proxy for feature importance in risk models
    """
    if column.is_target_candidate():
        return 3.0
    if column.is_identifier_like():
        return 0.2
    if column.is_constant_like():
        return 0.1
    return 1.0


def drift_severity(drift_score, weight):
    weighted = drift_score * weight

    if weighted > 1.0:
        return "CRITICAL"
    if weighted > 0.5:
        return "WARN"
    return "INFO"