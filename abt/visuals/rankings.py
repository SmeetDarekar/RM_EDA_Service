import matplotlib.pyplot as plt

def plot_drift_ranking(drift_scores: dict):
    """
    drift_scores: { feature_name: composite_drift_score }
    """
    features = list(drift_scores.keys())
    scores = list(drift_scores.values())

    plt.figure(figsize=(8, 5))
    plt.barh(features, scores)
    plt.xlabel("Composite Drift Score")
    plt.title("Feature Drift Ranking")
    plt.tight_layout()
    plt.show()