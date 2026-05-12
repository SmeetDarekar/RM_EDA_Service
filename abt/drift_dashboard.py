# abt/drift_dashboard.py

def _fmt(v):
    return f"{v:.4f}" if isinstance(v, (int, float)) else "NA"


def stddev_drift(abt_reg, abt_bkt, abt_mod):
    print("\n===== STANDARD DEVIATION DRIFT =====\n")
    print(
        f"{'COLUMN':30}"
        f"{'REG_STD':>12}"
        f"{'BKT_STD':>12}"
        f"{'MOD_STD':>12}"
        f"{'Δ REG→BKT':>12}"
        f"{'Δ BKT→MOD':>12}"
        f"{'Δ REG→MOD':>12}"
    )
    print("-" * 90)

    for col in set(abt_reg.columns) & set(abt_bkt.columns) & set(abt_mod.columns):
        r, b, m = abt_reg.columns[col], abt_bkt.columns[col], abt_mod.columns[col]

        if r.std is None or b.std is None or m.std is None:
            continue

        print(
            f"{col:30}"
            f"{_fmt(r.std):>12}"
            f"{_fmt(b.std):>12}"
            f"{_fmt(m.std):>12}"
            f"{_fmt(b.std - r.std):>12}"
            f"{_fmt(m.std - b.std):>12}"
            f"{_fmt(m.std - r.std):>12}"
        )


def tail_drift(abt_reg, abt_bkt, abt_mod):
    print("\n===== TAIL BEHAVIOR DRIFT (SKEWNESS / KURTOSIS) =====\n")
    print(
        f"{'COLUMN':30}"
        f"{'REG_SKEW':>12}"
        f"{'MOD_SKEW':>12}"
        f"{'Δ SKEW':>12}"
        f"{'REG_KURT':>14}"
        f"{'MOD_KURT':>14}"
        f"{'Δ KURT':>14}"
    )
    print("-" * 110)

    for col in set(abt_reg.columns) & set(abt_mod.columns):
        r, m = abt_reg.columns[col], abt_mod.columns[col]

        skew_r = r.attrs.get("skewness")
        skew_m = m.attrs.get("skewness")
        kurt_r = r.attrs.get("kurtosis")
        kurt_m = m.attrs.get("kurtosis")

        if skew_r is None or skew_m is None or kurt_r is None or kurt_m is None:
            continue

        print(
            f"{col:30}"
            f"{_fmt(skew_r):>12}"
            f"{_fmt(skew_m):>12}"
            f"{_fmt(skew_m - skew_r):>12}"
            f"{_fmt(kurt_r):>14}"
            f"{_fmt(kurt_m):>14}"
            f"{_fmt(kurt_m - kurt_r):>14}"
        )


def combined_drift_dashboard(abt_reg, abt_bkt, abt_mod):
    print("\n===== COMBINED DRIFT DASHBOARD =====\n")
    print(
        f"{'COLUMN':30}"
        f"{'Δ MEAN':>10}"
        f"{'Δ STD':>10}"
        f"{'Δ KURT':>12}"
        f"{'OUTLIER Δ':>12}"
        f"{'MISS Δ (%)':>12}"
    )
    print("-" * 90)

    for col in set(abt_reg.columns) & set(abt_mod.columns):
        r, m = abt_reg.columns[col], abt_mod.columns[col]

        if r.mean is None or m.mean is None:
            continue

        mean_d = m.mean - r.mean
        std_d = (m.std - r.std) if r.std and m.std else None
        kurt_d = (
            m.attrs.get("kurtosis") - r.attrs.get("kurtosis")
            if r.attrs.get("kurtosis") and m.attrs.get("kurtosis")
            else None
        )
        out_d = (
            m.outliers - r.outliers
            if r.outliers is not None and m.outliers is not None
            else None
        )
        miss_d = (
            m.missing_pct - r.missing_pct
            if r.missing_pct is not None and m.missing_pct is not None
            else None
        )

        print(
            f"{col:30}"
            f"{_fmt(mean_d):>10}"
            f"{_fmt(std_d):>10}"
            f"{_fmt(kurt_d):>12}"
            f"{_fmt(out_d):>12}"
            f"{_fmt(miss_d):>12}"
        )
