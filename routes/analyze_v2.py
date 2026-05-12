from flask import Blueprint, request, render_template, jsonify

from services.ic_client import fetch_table_metadata
from services.snapshot_store import snapshot_exists, save_snapshot, load_snapshot
from abt.snapshot import ABTSnapshot

from abt.analyze_engine import compute_single_abt_metrics
from abt.rule_engine import evaluate_single_abt_rules

analyze_v2_bp = Blueprint("analyze_v2", __name__)

CONTROLLED_CASLIB = "PUBLIC"


@analyze_v2_bp.route("/analyze_v2", methods=["POST"])
def analyze_v2():

    table = request.form.get("table") or (
        request.get_json(silent=True) or {}
    ).get("table")

    if not table:
        return jsonify({"error": "Table name required"}), 400

    if snapshot_exists(CONTROLLED_CASLIB, table):
        raw = load_snapshot(CONTROLLED_CASLIB, table)
        status = "Using previously analyzed snapshot"
    else:
        raw = fetch_table_metadata(table_name=table)
        if raw is None:
            return jsonify({"error": "Table not found"}), 404
        save_snapshot(CONTROLLED_CASLIB, table, raw)
        status = "Fetched metadata from Information Catalog"

    abt = ABTSnapshot(
        name=table,
        stage="ANALYZE",
        fetched_at=raw.get("analysisTimeStamp") or raw.get("fetchedAt"),
        raw_items=raw["items"]
    )

    metrics = compute_single_abt_metrics(abt)
    insights = evaluate_single_abt_rules(metrics)

    if request.form:
        return render_template(
            "analyze_v2.html",
            table=table,
            caslib=CONTROLLED_CASLIB,
            status=status,
            insights=insights,
        )

    return jsonify({
        "table": table,
        "caslib": CONTROLLED_CASLIB,
        "status": status,
        "insights": insights
    })