# abt/comparator.py

class ABTComparator:
    """
    Compares two ABT snapshots at metadata level.
    This is a STRICT 2-table comparator.
    """

    def __init__(self, abt_base, abt_compare):
        self.base = abt_base
        self.compare = abt_compare

        self.base_cols = set(abt_base.columns.keys())
        self.compare_cols = set(abt_compare.columns.keys())

    # --------------------------------------------------
    # Structural differences
    # --------------------------------------------------
    def missing_columns(self):
        """
        Columns present in base but missing in compare.
        """
        return sorted(self.base_cols - self.compare_cols)

    def additional_columns(self):
        """
        Columns present in compare but not in base.
        """
        return sorted(self.compare_cols - self.base_cols)

    # --------------------------------------------------
    # Statistical differences (best-effort)
    # --------------------------------------------------
    def compare_stats(self):
        """
        Compare available statistics for common columns.
        Only compares metrics that exist on BOTH sides.
        """

        diffs = {}

        common = self.base_cols & self.compare_cols

        for col in common:
            base_col = self.base.columns[col]
            comp_col = self.compare.columns[col]

            col_diffs = {}

            # Standard deviation
            if (
                base_col.std is not None
                and comp_col.std is not None
            ):
                col_diffs["std_delta"] = comp_col.std - base_col.std

            # Missingness
            if (
                base_col.missing_pct is not None
                and comp_col.missing_pct is not None
            ):
                col_diffs["missing_pct_delta"] = (
                    comp_col.missing_pct - base_col.missing_pct
                )

            if col_diffs:
                diffs[col] = col_diffs

        return diffs

    # --------------------------------------------------
    # ABT-level summary metric
    # --------------------------------------------------
    def completeness_score(self):
        """
        Simple comparability indicator.
        """

        missing = len(self.missing_columns())
        additional = len(self.additional_columns())
        common = len(self.base_cols & self.compare_cols)

        if common == 0:
            return "NOT COMPARABLE"

        if missing == 0 and additional == 0:
            return "FULLY COMPARABLE"

        if missing > common * 0.3:
            return "MAJOR STRUCTURAL CHANGE"

        return "PARTIALLY COMPARABLE"