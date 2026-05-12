import matplotlib.pyplot as plt

def abt_drift_summary(drift_scores):
    total = len(drift_scores)
    high = sum(1 for v in drift_scores.values() if v > 1.0)
    medium = sum(1 for v in drift_scores.values() if 0.5 < v <= 1.0)
    low = total - high - medium

    plt.figure(figsize=(5, 5))
    plt.pie(
        [high, medium, low],
        labels=["High Drift", "Medium Drift", "Low/None"],
        autopct="%1.1f%%"
    )
    plt.title("ABT Drift Severity Distribution")
    plt.show()