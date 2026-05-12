import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def missingness_heatmap(abt_reg, abt_bkt, abt_mod):
    data = []

    for col in set(abt_reg.columns) & set(abt_bkt.columns) & set(abt_mod.columns):
        data.append({
            "feature": col,
            "REG": abt_reg.columns[col].missing_pct,
            "BKT": abt_bkt.columns[col].missing_pct,
            "MOD": abt_mod.columns[col].missing_pct
        })

    df = pd.DataFrame(data).set_index("feature")

    plt.figure(figsize=(8, max(4, len(df)*0.3)))
    sns.heatmap(df, annot=True, cmap="YlGnBu")
    plt.title("Missingness (%) Across ABT Stages")
    plt.tight_layout()
    plt.show()