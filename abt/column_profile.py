# abt/column_profile.py

class ColumnProfile:
    """
    Risk-aware, defensive column profile built from
    SAS Information Catalog metadata.
    """

    def __init__(self, name: str, attrs: dict):
        self.name = name
        attrs = attrs or {}

        # -------------------------
        # Core statistics
        # -------------------------
        self.mean = attrs.get("mean")
        self.std = attrs.get("standardDeviation")
        self.min = attrs.get("min")
        self.max = attrs.get("max")
        self.median = attrs.get("median")

        # -------------------------
        # Distribution shape
        # -------------------------
        self.skewness = attrs.get("skewness")
        self.kurtosis = attrs.get("kurtosis")
        self.outliers = attrs.get("nOutliers")

        # -------------------------
        # Quantiles (optional)
        # -------------------------
        self.q25 = attrs.get("quantiles25")
        self.q75 = attrs.get("quantiles75")

        # -------------------------
        # Data quality (FIXED)
        # -------------------------
        self.completeness_pct = attrs.get("completenessPercent")

        if self.completeness_pct is not None:
            self.missing_pct = round(100 - self.completeness_pct, 2)
        else:
            self.missing_pct = None

        self.cardinality = attrs.get("cardinalityCount")

        # -------------------------
        # Semantic hints
        # -------------------------
        self.scale = attrs.get("statisticalScale")
        self.semantic = attrs.get("semanticTypeId")

        self.has_unique = attrs.get("hasUniqueField", False)

    # --------------------------------------------------
    # Helper methods (safe checks)
    # --------------------------------------------------

    def has_outlier_info(self):
        return self.outliers is not None

    def has_distribution_shape(self):
        return self.skewness is not None or self.kurtosis is not None

    def has_variance(self):
        return self.std is not None

    def is_constant_like(self):
        return self.std == 0 or self.scale == "unary"

    def is_identifier_like(self):
        return self.scale == "id"

    def is_target_candidate(self):
        return "OUTCOME" in self.name.upper()