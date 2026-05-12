def derive_visual_observations(column_name, reg, bkt, mod):
    """
    Generate human-style observations that would be evident from plots.
    These are deterministic and auditable.
    """

    observations = []

    # ---- Variance / Boxplot interpretation ----
    if reg.std and mod.std and mod.std < 0.5 * reg.std:
        observations.append(
            "Boxplot indicates strong variance compression at the model stage"
        )

    # ---- Tail behavior from KDE / histograms ----
    if (
        reg.attrs.get("kurtosis") is not None
        and mod.attrs.get("kurtosis") is not None
        and mod.attrs["kurtosis"] < 0.5 * reg.attrs["kurtosis"]
    ):
        observations.append(
            "Distribution plots indicate a substantial reduction in tail heaviness at the model stage"
        )

    # ---- Nesting / overlap pattern ----
    if reg.std and bkt.std and mod.std:
        if mod.std < bkt.std < reg.std:
            observations.append(
                "Overlaid distribution plots show the model-stage distribution nested within earlier stages"
            )

    # ---- Missingness heatmap interpretation ----
    if (
        reg.missing_pct is not None
        and mod.missing_pct is not None
        and mod.missing_pct > reg.missing_pct + 5
    ):
        observations.append(
            "Missingness heatmap shows improved completeness at the model stage"
        )

    return observations