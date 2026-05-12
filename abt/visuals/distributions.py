import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_distribution_overlap(feature, reg_vals, bkt_vals, mod_vals):
    df = pd.DataFrame({
        "value": reg_vals + bkt_vals + mod_vals,
        "stage": (
            ["REG"] * len(reg_vals) +
            ["BKT"] * len(bkt_vals) +
            ["MOD"] * len(mod_vals)
        )
    })

    plt.figure(figsize=(8, 5))
    sns.kdeplot(data=df, x="value", hue="stage", common_norm=False)
    plt.title(f"Distribution Overlap: {feature}")
    plt.tight_layout()
    plt.show()


def plot_boxplot(feature, reg_vals, bkt_vals, mod_vals):
    df = pd.DataFrame({
        "value": reg_vals + bkt_vals + mod_vals,
        "stage": (
            ["REG"] * len(reg_vals) +
            ["BKT"] * len(bkt_vals) +
            ["MOD"] * len(mod_vals)
        )
    })

    plt.figure(figsize=(6, 5))
    sns.boxplot(data=df, x="stage", y="value")
    plt.title(f"Boxplot Across Stages: {feature}")
    plt.tight_layout()
    plt.show()