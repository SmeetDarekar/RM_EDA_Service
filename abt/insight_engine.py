# # abt/insights.py

# from abt.metrics import composite_drift, stage_pattern
# from abt.scoring import feature_risk_weight, drift_severity
# from abt.narrator import narrate_insight


# def generate_insights(abt_reg, abt_bkt, abt_mod):
#     insights = []

#     common_cols = (
#         set(abt_reg.columns)
#         & set(abt_bkt.columns)
#         & set(abt_mod.columns)
#     )

#     for col_name in common_cols:
#         reg = abt_reg.columns[col_name]
#         bkt = abt_bkt.columns[col_name]
#         mod = abt_mod.columns[col_name]

#         # ---------- Drift metrics ----------
#         reg_bkt_score, _ = composite_drift(reg, bkt)
#         bkt_mod_score, _ = composite_drift(bkt, mod)
#         reg_mod_score, components = composite_drift(reg, mod)

#         pattern = stage_pattern(
#             reg_bkt_score, bkt_mod_score, reg_mod_score
#         )

#         weight = feature_risk_weight(mod)
#         severity = drift_severity(reg_mod_score, weight)

#         # ---------- Evidence collection ----------
#         observed = []

#         if reg.std and mod.std and mod.std < 0.5 * reg.std:
#             observed.append(
#                 "Variance reduces sharply at model stage while central tendency remains stable"
#             )

#         if reg.outliers and mod.outliers is not None and mod.outliers < reg.outliers * 0.5:
#             observed.append(
#                 "Number of extreme values reduces significantly in later stage"
#             )

#         if bkt.missing_pct and mod.missing_pct and mod.missing_pct > bkt.missing_pct:
#             observed.append(
#                 "Data completeness improves after back-testing stage"
#             )

#         # ---------- Evidence‑First Narration ----------

#         # TARGET / OUTCOME risk
#         if mod.is_target_candidate() and pattern == "MODEL_STAGE_INFLECTION":
#             insights.append(
#                 narrate_insight(
#                     column_name=col_name,
#                     severity="CRITICAL",
#                     category="TARGET_INTEGRITY_RISK",
#                     stage_span="BACKTEST → MODEL",

#                     observed_behavior=observed or [
#                         "Target distribution changes significantly at model stage"
#                     ],

#                     pattern="Post‑backtest outcome stabilization pattern",

#                     likely_cause=(
#                         "Outcome variable appears to be altered or conditioned "
#                         "after back-testing, possibly due to post-event availability "
#                         "or target construction logic applied at model build time"
#                     ),

#                     risk_implication=[
#                         "Back-testing performance metrics may be inflated",
#                         "Target definition may not generalize to production scoring",
#                         "Additional regulatory scrutiny likely during validation"
#                     ],

#                     recommended_action=(
#                         "Review target construction logic between back-testing "
#                         "and model training stages before proceeding to approval"
#                     ),

#                     evidence={
#                         "composite_drift_components": components,
#                         "reg_bkt_score": reg_bkt_score,
#                         "bkt_mod_score": bkt_mod_score
#                     }
#                 )
#             )

#         # ---------- High‑impact feature drift ----------
#         elif severity == "CRITICAL":
#             insights.append(
#                 narrate_insight(
#                     column_name=col_name,
#                     severity=severity,
#                     category="FEATURE_STABILITY_RISK",
#                     stage_span="REGISTRY → MODEL",

#                     observed_behavior=observed or [
#                         "Significant distributional change observed across ABT lifecycle"
#                     ],

#                     pattern="High composite drift in risk‑relevant feature",

#                     likely_cause=(
#                         "Feature behavior suggests transformation or population mismatch "
#                         "introduced during ABT progression"
#                     ),

#                     risk_implication=[
#                         "Model coefficients or splits may be unstable",
#                         "Future population may not align with training data"
#                     ],

#                     recommended_action=(
#                         "Inspect feature transformation logic and verify population "
#                         "consistency across ABT stages"
#                     ),

#                     evidence={
#                         "composite_drift_components": components,
#                         "reg_mod_score": reg_mod_score
#                     }
#                 )
#             )

#     return insights














# abt/insights.py

# from abt.metrics import composite_drift, stage_pattern
# from abt.scoring import feature_risk_weight, drift_severity
# from abt.narrator import narrate_insight
# from abt.visuals.visual_observations import derive_visual_observations


# def generate_insights(abt_reg, abt_bkt, abt_mod):
#     """
#     Generate evidence-first, risk-grade insights by comparing
#     ABT snapshots across Registry, Backtest, and Model stages.
#     """

#     insights = []

#     common_cols = (
#         set(abt_reg.columns)
#         & set(abt_bkt.columns)
#         & set(abt_mod.columns)
#     )

#     for col_name in sorted(common_cols):
#         reg = abt_reg.columns[col_name]
#         bkt = abt_bkt.columns[col_name]
#         mod = abt_mod.columns[col_name]

#         # --------------------------------------------------
#         # Drift metrics (numeric, non-visual)
#         # --------------------------------------------------
#         reg_bkt_score, _ = composite_drift(reg, bkt)
#         bkt_mod_score, _ = composite_drift(bkt, mod)
#         reg_mod_score, components = composite_drift(reg, mod)

#         pattern = stage_pattern(
#             reg_bkt_score,
#             bkt_mod_score,
#             reg_mod_score
#         )

#         weight = feature_risk_weight(mod)
#         severity = drift_severity(reg_mod_score, weight)

#         # --------------------------------------------------
#         # Observed statistical behavior (textual evidence)
#         # --------------------------------------------------
#         observed = []

#         if reg.std and mod.std and mod.std < 0.5 * reg.std:
#             observed.append(
#                 "Variance reduces sharply at model stage while central tendency remains broadly stable"
#             )

#         if (
#             reg.outliers is not None
#             and mod.outliers is not None
#             and reg.outliers > 0
#             and mod.outliers < 0.5 * reg.outliers
#         ):
#             observed.append(
#                 "Number of extreme values reduces substantially in later stage"
#             )

#         if (
#             bkt.missing_pct is not None
#             and mod.missing_pct is not None
#             and mod.missing_pct > bkt.missing_pct
#         ):
#             observed.append(
#                 "Data completeness improves after back-testing stage"
#             )

#         if not observed:
#             observed.append(
#                 "Material distributional changes observed across ABT lifecycle"
#             )

#         # --------------------------------------------------
#         # Visual evidence (what plots would show)
#         # --------------------------------------------------
#         visual_observations = derive_visual_observations(
#             column_name=col_name,
#             reg=reg,
#             bkt=bkt,
#             mod=mod
#         )

#         # --------------------------------------------------
#         # TARGET / OUTCOME integrity risk
#         # --------------------------------------------------
#         if mod.is_target_candidate() and pattern == "MODEL_STAGE_INFLECTION":
#             insights.append(
#                 narrate_insight(
#                     column_name=col_name,
#                     severity="CRITICAL",
#                     category="TARGET_INTEGRITY_RISK",
#                     stage_span="BACKTEST → MODEL",

#                     observed_behavior=observed,

#                     pattern="Post-backtest outcome stabilization pattern",

#                     likely_cause=(
#                         "Outcome variable behavior changes after the back-testing stage, "
#                         "potentially due to post-event availability, target conditioning, "
#                         "or transformation logic applied during model training"
#                     ),

#                     risk_implication=[
#                         "Back-testing performance metrics may overstate true model robustness",
#                         "Target definition may not remain consistent at scoring time",
#                         "Model validation and regulatory confidence may be impacted"
#                     ],

#                     recommended_action=(
#                         "Review target construction and filtering logic applied between "
#                         "back-testing and model training stages before approval"
#                     ),

#                     evidence={
#                         "composite_drift_components": components,
#                         "stage_drift_scores": {
#                             "reg_to_bkt": reg_bkt_score,
#                             "bkt_to_mod": bkt_mod_score,
#                             "reg_to_mod": reg_mod_score
#                         },
#                         "visual_observations": visual_observations
#                     }
#                 )
#             )

#         # --------------------------------------------------
#         # High-impact feature stability risk (non-target)
#         # --------------------------------------------------
#         elif severity == "CRITICAL":
#             insights.append(
#                 narrate_insight(
#                     column_name=col_name,
#                     severity=severity,
#                     category="FEATURE_STABILITY_RISK",
#                     stage_span="REGISTRY → MODEL",

#                     observed_behavior=observed,

#                     pattern="High composite drift in risk-relevant feature",

#                     likely_cause=(
#                         "Feature behavior suggests transformation effects, population "
#                         "misalignment, or distributional instability introduced during "
#                         "ABT progression"
#                     ),

#                     risk_implication=[
#                         "Model parameters may be unstable or over-fitted",
#                         "Performance observed during training may not generalize",
#                         "Downstream monitoring thresholds may be unreliable"
#                     ],

#                     recommended_action=(
#                         "Inspect feature construction and population consistency across "
#                         "ABT stages before relying on this variable in the model"
#                     ),

#                     evidence={
#                         "composite_drift_components": components,
#                         "reg_to_mod_drift_score": reg_mod_score,
#                         "visual_observations": visual_observations
#                     }
#                 )
#             )

#     return insights


















# abt/insight_engine.py

from abt.metrics import composite_drift, stage_pattern
from abt.scoring import feature_risk_weight, drift_severity
from abt.narrator import narrate_insight
from abt.visuals.visual_observations import derive_visual_observations


def generate_insights(abt_reg, abt_bkt, abt_mod):
    """
    Generate evidence-first, risk-grade insights by comparing
    ABT snapshots across Registry, Backtest, and Model stages.
    """

    insights = []

    common_cols = (
        set(abt_reg.columns)
        & set(abt_bkt.columns)
        & set(abt_mod.columns)
    )

    for col_name in sorted(common_cols):
        reg = abt_reg.columns[col_name]
        bkt = abt_bkt.columns[col_name]
        mod = abt_mod.columns[col_name]

        # --------------------------------------------------
        # Drift metrics (safe – composite_drift already guards)
        # --------------------------------------------------
        reg_bkt_score, _ = composite_drift(reg, bkt)
        bkt_mod_score, _ = composite_drift(bkt, mod)
        reg_mod_score, components = composite_drift(reg, mod)

        pattern = stage_pattern(
            reg_bkt_score,
            bkt_mod_score,
            reg_mod_score
        )

        weight = feature_risk_weight(mod)
        severity = drift_severity(reg_mod_score, weight)

        # --------------------------------------------------
        # Observed statistical behavior (DEFENSIVE)
        # --------------------------------------------------
        observed = []

        # Variance behavior
        if reg.has_variance() and mod.has_variance():
            if mod.std < 0.5 * reg.std:
                observed.append(
                    "Variance reduces sharply at model stage while central tendency remains broadly stable"
                )

        # Outlier behavior
        if reg.has_outlier_info() and mod.has_outlier_info():
            if reg.outliers > 0 and mod.outliers < 0.5 * reg.outliers:
                observed.append(
                    "Number of extreme values reduces substantially in later stage"
                )

        # Completeness / data quality
        if (
            bkt.missing_pct is not None
            and mod.missing_pct is not None
            and mod.missing_pct > bkt.missing_pct
        ):
            observed.append(
                "Data completeness improves after back-testing stage"
            )

        # Fallback if no concrete signals
        if not observed:
            observed.append(
                "No strong distributional or quality signals detected across stages"
            )

        # --------------------------------------------------
        # Visual evidence (derive_visual_observations is defensive)
        # --------------------------------------------------
        visual_observations = derive_visual_observations(
            column_name=col_name,
            reg=reg,
            bkt=bkt,
            mod=mod
        )

        # --------------------------------------------------
        # TARGET / OUTCOME integrity risk
        # --------------------------------------------------
        if mod.is_target_candidate() and pattern == "MODEL_STAGE_INFLECTION":
            insights.append(
                narrate_insight(
                    column_name=col_name,
                    severity="CRITICAL",
                    category="TARGET_INTEGRITY_RISK",
                    stage_span="BACKTEST → MODEL",

                    observed_behavior=observed,
                    pattern="Post-backtest outcome stabilization pattern",

                    likely_cause=(
                        "Outcome variable behavior changes after the back-testing stage, "
                        "potentially due to post-event availability, target conditioning, "
                        "or transformation logic applied during model training"
                    ),

                    risk_implication=[
                        "Back-testing performance metrics may overstate true model robustness",
                        "Target definition may not remain consistent at scoring time",
                        "Model validation and regulatory confidence may be impacted"
                    ],

                    recommended_action=(
                        "Review target construction and filtering logic applied between "
                        "back-testing and model training stages before approval"
                    ),

                    evidence={
                        "composite_drift_components": components,
                        "stage_drift_scores": {
                            "reg_to_bkt": reg_bkt_score,
                            "bkt_to_mod": bkt_mod_score,
                            "reg_to_mod": reg_mod_score
                        },
                        "visual_observations": visual_observations
                    }
                )
            )

        # --------------------------------------------------
        # High-impact feature stability risk (non-target)
        # --------------------------------------------------
        elif severity == "CRITICAL":
            insights.append(
                narrate_insight(
                    column_name=col_name,
                    severity=severity,
                    category="FEATURE_STABILITY_RISK",
                    stage_span="REGISTRY → MODEL",

                    observed_behavior=observed,
                    pattern="High composite drift in risk-relevant feature",

                    likely_cause=(
                        "Feature behavior suggests transformation effects, population "
                        "misalignment, or distributional instability introduced during "
                        "ABT progression"
                    ),

                    risk_implication=[
                        "Model parameters may be unstable or over-fitted",
                        "Performance observed during training may not generalize",
                        "Downstream monitoring thresholds may be unreliable"
                    ],

                    recommended_action=(
                        "Inspect feature construction and population consistency across "
                        "ABT stages before relying on this variable in the model"
                    ),

                    evidence={
                        "composite_drift_components": components,
                        "reg_to_mod_drift_score": reg_mod_score,
                        "visual_observations": visual_observations
                    }
                )
            )

    return insights