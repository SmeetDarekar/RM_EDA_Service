# from pathlib import Path

# from abt.loader import load_json
# from abt.models import ABTSnapshot
# from abt.insight_engine import generate_insights

# def build_snapshot(path, stage):
#     raw = load_json(path)

#     return ABTSnapshot(
#         name=raw.get("tableName"),
#         stage=stage,
#         fetched_at=raw.get("fetchedAt"),
#         items=raw["data"]["items"]
#     )

# if __name__ == "__main__":
#     reg = build_snapshot(Path("data/abt_reg.json"), "REGISTRY")
#     bkt = build_snapshot(Path("data/abt_bkt.json"), "BACKTEST")
#     mod = build_snapshot(Path("data/abt_mod.json"), "MODEL")

#     insights = generate_insights(reg, bkt, mod)

#     print("\n===== ABT INSIGHTS =====\n")
#     if not insights:
#         print("No major risk issues detected.")
#     else:
#         for i in insights:
#             print(f"[{i['severity']}] {i['category']} | {i['column']}")
#             print(f"  → {i['message']}\n")













# run.py (only the printing part changes)

from pathlib import Path
from abt.loader import load_json
from abt.models import ABTSnapshot
from abt.insight_engine import generate_insights

from abt.visuals.rankings import plot_drift_ranking
from abt.visuals.quality import missingness_heatmap
from abt.visuals.dashboard import abt_drift_summary

from abt.llm.ollama_client import call_ollama
from abt.llm.prompts import risk_insight_prompt



def build_snapshot(path, stage):
    raw = load_json(path)
    return ABTSnapshot(
        name=raw.get("tableName"),
        stage=stage,
        fetched_at=raw.get("fetchedAt"),
        items=raw["data"]["items"]
    )


def print_insight(insight):
    print("=" * 70)
    print(f"SEVERITY : {insight['severity']}")
    print(f"CATEGORY : {insight['category']}")
    print(f"COLUMN   : {insight['column']}")
    print(f"STAGE    : {insight.get('stage', 'N/A')}\n")

    print("Observed behavior:")
    for obs in insight["observed_behavior"]:
        print(f"  - {obs}")
    print()

    print(f"Detected pattern:\n  {insight['detected_pattern']}\n")
    print(f"Likely cause:\n  {insight['likely_cause']}\n")

    print("Risk implication:")
    for r in insight["risk_implication"]:
        print(f"  - {r}")
    print()

    print(f"Recommended action:\n  {insight['recommended_action']}\n")


if __name__ == "__main__":
    reg = build_snapshot(Path("data/abt_reg.json"), "REGISTRY")
    bkt = build_snapshot(Path("data/abt_bkt.json"), "BACKTEST")
    mod = build_snapshot(Path("data/abt_mod.json"), "MODEL")

    insights = generate_insights(reg, bkt, mod)

    print("\n===== ABT INSIGHTS =====\n")
    if not insights:
        print("✅ No significant risk issues detected.")
    else:
        for ins in insights:
            print_insight(ins)


from abt.drift_dashboard import (
    stddev_drift,
    tail_drift,
    combined_drift_dashboard
)

# Diagnostic drift views (for transparency/debugging)
stddev_drift(reg, bkt, mod)
tail_drift(reg, bkt, mod)
combined_drift_dashboard(reg, bkt, mod)


# Example: visualization inputs
drift_scores = {
    i["column"]: i["evidence"]["composite_drift_components"]["std"]
    for i in insights
    if "evidence" in i
}

plot_drift_ranking(drift_scores)
abt_drift_summary(drift_scores)
missingness_heatmap(reg, bkt, mod)



print("\n===== LLM‑GENERATED NARRATION (OLLAMA) =====\n")

for insight in insights:
    prompt = risk_insight_prompt(insight)
    explanation = call_ollama(prompt)

    print("-" * 80)
    print(explanation)
    print()
