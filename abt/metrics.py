# abt/metrics.py

def safe_pct_change(v1, v2, eps=1e-9):
    if v1 is None or v2 is None:
        return 0.0
    denom = abs(v1) if abs(v1) > eps else eps
    return abs(v2 - v1) / denom


def composite_drift(col_a, col_b):
    """
    Composite Drift Index (CDI)
    Captures distribution shape change without raw data.
    """

    drift_components = {
        "mean": safe_pct_change(col_a.mean, col_b.mean),
        "std": safe_pct_change(col_a.std, col_b.std),
        "skewness": safe_pct_change(
            col_a.attrs.get("skewness"),
            col_b.attrs.get("skewness")
        ),
        "kurtosis": safe_pct_change(
            col_a.attrs.get("kurtosis"),
            col_b.attrs.get("kurtosis")
        ),
        "outliers": safe_pct_change(
            col_a.outliers,
            col_b.outliers
        )
    }

    # Weighted sum – tuned for risk modelling
    weights = {
        "mean": 0.2,
        "std": 0.3,
        "skewness": 0.2,
        "kurtosis": 0.2,
        "outliers": 0.1
    }

    score = sum(weights[k] * drift_components[k] for k in drift_components)

    return score, drift_components


def stage_pattern(reg_score, bkt_score, mod_score):
    """
    Classify drift behavior across REG → BKT → MOD
    """

    if reg_score < 0.2 and bkt_score < 0.2 and mod_score < 0.2:
        return "STABLE"

    if reg_score < bkt_score < mod_score:
        return "PROGRESSIVE_DRIFT"

    if reg_score < 0.2 and bkt_score < 0.2 and mod_score > 0.5:
        return "MODEL_STAGE_INFLECTION"

    if reg_score < bkt_score and mod_score < bkt_score:
        return "FILTER_THEN_STABLE"

    return "IRREGULAR"
