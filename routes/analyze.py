from flask import Blueprint, request, render_template, jsonify

from abt.llm.prompts import analyze_abt_prompt
from abt.llm.ollama_client import call_ollama

from abt.analyze_engine import generate_single_abt_insights
from services.ic_client import fetch_table_metadata
from services.snapshot_store import (
    snapshot_exists,
    save_snapshot,
    load_snapshot
)
from abt.snapshot import ABTSnapshot
from abt.target_detection import detect_target_column_from_dump
#from abt.column_kpi_insights import generate_column_kpi_insights

from abt.column_kpi_insights import (
    generate_analyze_column_kpi_insights,
    filter_analyze_column_kpi_insights
)


analyze_bp = Blueprint("analyze", __name__)

CONTROLLED_CASLIB = "PUBLIC"


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze a single ABT using IC metadata.
    CASLIB is implicit and controlled.
    """

    # -----------------------------
    # Input
    # -----------------------------
    table = request.form.get("table") or (
        request.get_json(silent=True) or {}
    ).get("table")

    user_selected_target = request.form.get("target")

    if not table:
        msg = "Table name is required for analysis"
        return render_template("analyze.html", error=msg)

    # -----------------------------
    # Snapshot handling
    # -----------------------------
    if snapshot_exists(CONTROLLED_CASLIB, table):
        raw = load_snapshot(CONTROLLED_CASLIB, table)
        status = "Using previously analyzed snapshot"
    else:
        raw = fetch_table_metadata(table_name=table)

        if raw is None:
            return render_template(
                "analyze.html",
                error="Table not found in Information Catalog"
            )

        save_snapshot(CONTROLLED_CASLIB, table, raw)
        status = "Fetched metadata from Information Catalog"

    abt = ABTSnapshot(
        name=table,
        stage="ANALYZE",
        fetched_at=raw.get("analysisTimeStamp") or raw.get("fetchedAt"),
        raw_items=raw["items"],
    )

    # -----------------------------
    # Task 1.1 — Target detection
    # -----------------------------
    target_info = detect_target_column_from_dump(raw["items"])

    # -----------------------------
    # Task 1.2 — User selection
    # -----------------------------
    if target_info["status"] in ("NOT_FOUND", "AMBIGUOUS"):
        if not user_selected_target:
            return render_template(
                "select_target.html",
                table=table,
                reason=target_info["reason"],
                candidates=target_info["candidates"],
                all_columns=target_info["all_columns"]
            )
        else:
            target_info = {
                "status": "USER_SELECTED",
                "target": user_selected_target
            }

    # -----------------------------
    # Analysis (UNCHANGED)
    # -----------------------------
    insights = generate_single_abt_insights(abt)

    llm_explanation = call_ollama(
        analyze_abt_prompt({
            "summary": {
                "table": table,
                "total_columns": len(abt.columns),
            },
            "findings": insights
        })
    )


    # We are tring the new KPI interpretation here
    #column_kpi_insights = generate_column_kpi_insights(base_snapshot=abt)

    
    raw_column_kpis = generate_analyze_column_kpi_insights(abt)
    column_kpi_insights = filter_analyze_column_kpi_insights(raw_column_kpis)


    return render_template(
        "analyze.html",
        table=table,
        caslib=CONTROLLED_CASLIB,
        status=status,
        insights=insights,
        llm_explanation=llm_explanation,
        column_kpi_insights = column_kpi_insights
    )