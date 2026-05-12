class ColumnProfile:
    def __init__(self, name: str, attrs: dict):
        self.name = name
        self.attrs = attrs or {}

        self.mean = self.attrs.get("mean")
        self.std = self.attrs.get("standardDeviation")
        self.missing_pct = self.attrs.get("completenessPercent")
        self.uniqueness_pct = self.attrs.get("uniquenessPercent")
        self.cardinality = self.attrs.get("cardinalityCount")
        self.scale = self.attrs.get("statisticalScale")
        self.semantic = self.attrs.get("semanticTypeId")
        self.outliers = self.attrs.get("nOutliers")

    # ---------- Risk-aware helpers ----------

    def is_identifier_like(self):
        return (
            self.scale == "id"
            or (self.uniqueness_pct is not None and self.uniqueness_pct > 95)
        )

    def is_constant_like(self):
        return self.scale == "unary" or self.std == 0

    def is_target_candidate(self):
        return "OUTCOME" in self.name.upper()

    def has_quality_issue(self):
        return self.missing_pct is not None and self.missing_pct < 95


class ABTSnapshot:
    def __init__(self, name: str, stage: str, fetched_at: str, items: list):
        self.name = name
        self.stage = stage
        self.fetched_at = fetched_at
        self.columns = self._build_columns(items)

    def _build_columns(self, items):
        cols = {}
        for item in items:
            col_name = item.get("name")
            attrs = item.get("attributes", {})
            cols[col_name] = ColumnProfile(col_name, attrs)
        return cols