# abt/snapshot.py

from abt.column_profile import ColumnProfile


class ABTSnapshot:
    """
    Represents a snapshot of an ABT at a specific lifecycle stage,
    built from SAS Information Catalog column-level metadata.
    """

    def __init__(self, name, stage, fetched_at, raw_items):
        """
        Parameters
        ----------
        name : str
            Table name

        stage : str
            Lifecycle stage (ANALYZE / BASE / COMPARE / REG / BKT / MODEL)

        fetched_at : str | None
            Timestamp from IC metadata

        raw_items : list[dict]
            IC /catalog/instances items (casColumn entities)
        """

        self.name = name
        self.stage = stage
        self.fetched_at = fetched_at

        # Normalize raw IC items into ColumnProfile objects
        self.columns = self._build_columns(raw_items)

    def _build_columns(self, raw_items):
        """
        Convert IC casColumn items into ColumnProfile objects.
        """
        columns = {}

        for item in raw_items:
            col_name = item.get("name")
            attributes = item.get("attributes", {})

            if not col_name:
                continue

            columns[col_name] = ColumnProfile(
                name=col_name,
                attrs=attributes
            )

        return columns
    
    def to_comparison_dict(self):
        return {
            "row_count": self.row_count,
            "entity_count": self.entity_count,
            "outcome_available_pct": self.outcome_available_pct,
            "columns": self.column_profiles,   # already computed profiles
            "lineage_columns": self.lineage_columns
        }