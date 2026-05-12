# # routes/analyze.py

# from flask import Blueprint, request, render_template, jsonify

# from abt.llm.prompts import analyze_abt_prompt
# from abt.llm.ollama_client import call_llm


# from abt.analyze_engine import generate_single_abt_insights
# from services.ic_client import fetch_table_metadata
# from services.snapshot_store import (
#     snapshot_exists,
#     save_snapshot,
#     load_snapshot
# )
# from abt.snapshot import ABTSnapshot
# from abt.insight_engine import generate_insights


# analyze_bp = Blueprint("analyze", __name__)

# # ------------------------------------------------------------------
# # Analyze operates on a SINGLE controlled CASLIB
# # ------------------------------------------------------------------
# CONTROLLED_CASLIB = "PUBLIC"


# @analyze_bp.route("/analyze", methods=["POST"])
# def analyze():
#     """
#     Analyze a single ABT using IC metadata.
#     CASLIB is implicit and controlled.
#     """

#     # --------------------------------------------------------------
#     # 1. Get user input (table name only)
#     # --------------------------------------------------------------
#     table = request.form.get("table") or (
#         request.get_json(silent=True) or {}
#     ).get("table")

#     if not table:
#         msg = "Table name is required for analysis"
#         if request.form:
#             return render_template("analyze.html", error=msg)
#         return jsonify({"error": msg}), 400

#     # --------------------------------------------------------------
#     # 2. Snapshot reuse or IC fetch
#     # --------------------------------------------------------------
#     if snapshot_exists(CONTROLLED_CASLIB, table):
#         raw = load_snapshot(CONTROLLED_CASLIB, table)
#         status = "Using previously analyzed snapshot"
#     else:
#         raw = fetch_table_metadata(
#             table_name=table
#         )

#         if raw is None:
#             msg = "Table not found in Information Catalog"
#             if request.form:
#                 return render_template("analyze.html", error=msg)
#             return jsonify({"error": msg}), 404

#         save_snapshot(CONTROLLED_CASLIB, table, raw)
#         status = "Fetched metadata from Information Catalog"

#     # --------------------------------------------------------------
#     # 3. Build ABT snapshot
#     # ✅ FIX IS HERE: raw["items"], NOT raw["data"]["items"]
#     # --------------------------------------------------------------
    
#     abt = ABTSnapshot(
#         name=table,
#         stage="ANALYZE",
#         fetched_at=raw.get("analysisTimeStamp") or raw.get("fetchedAt"),
#         raw_items=raw["items"],   # ✅ now valid
#     )

#     # --------------------------------------------------------------
#     # 4. Generate insights
#     # --------------------------------------------------------------
#     insights = generate_single_abt_insights(abt)

    

#     # --------------------------------------------------------------
#     # 5. Return response
#     # --------------------------------------------------------------
#     if request.form:
#         return render_template(
#             "analyze.html",
#             table=table,
#             caslib=CONTROLLED_CASLIB,
#             status=status,
#             insights=insights
#         )

#     return jsonify({
#         "table": table,
#         "caslib": CONTROLLED_CASLIB,
#         "status": status,
#         "insights": insights,
#     })




















# routes/analyze.py

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

analyze_bp = Blueprint("analyze", __name__)

# ------------------------------------------------------------------
# Analyze operates on a SINGLE controlled CASLIB
# ------------------------------------------------------------------
CONTROLLED_CASLIB = "PUBLIC"


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze a single ABT using IC metadata.
    CASLIB is implicit and controlled.
    """

    # --------------------------------------------------------------
    # 1. Get user input (table name only)
    # --------------------------------------------------------------
    table = request.form.get("table") or (
        request.get_json(silent=True) or {}
    ).get("table")

    if not table:
        msg = "Table name is required for analysis"
        if request.form:
            return render_template("analyze.html", error=msg)
        return jsonify({"error": msg}), 400

    # --------------------------------------------------------------
    # 2. Snapshot reuse or IC fetch
    # --------------------------------------------------------------
    if snapshot_exists(CONTROLLED_CASLIB, table):
        raw = load_snapshot(CONTROLLED_CASLIB, table)
        status = "Using previously analyzed snapshot"
    else:
        raw = fetch_table_metadata(table_name=table)

        if raw is None:
            msg = "Table not found in Information Catalog"
            if request.form:
                return render_template("analyze.html", error=msg)
            return jsonify({"error": msg}), 404

        save_snapshot(CONTROLLED_CASLIB, table, raw)
        status = "Fetched metadata from Information Catalog"

    # --------------------------------------------------------------
    # 3. Build ABT snapshot
    # --------------------------------------------------------------
    abt = ABTSnapshot(
        name=table,
        stage="ANALYZE",
        fetched_at=raw.get("analysisTimeStamp") or raw.get("fetchedAt"),
        raw_items=raw["items"],
    )

    # --------------------------------------------------------------
    # 4. Generate deterministic insights
    # --------------------------------------------------------------
    insights = generate_single_abt_insights(abt)

    # --------------------------------------------------------------
    # 5. Generate LLM explanation (TEXT ONLY)
    # --------------------------------------------------------------
    llm_explanation = call_ollama(
        analyze_abt_prompt({
            "summary": {
                "table": table,
                "total_columns": len(abt.columns),
            },
            "findings": insights
        })
    )

    # --------------------------------------------------------------
    # 6. Return response
    # --------------------------------------------------------------
    if request.form:
        return render_template(
            "analyze.html",
            table=table,
            caslib=CONTROLLED_CASLIB,
            status=status,
            insights=insights,
            llm_explanation=llm_explanation
        )

    return jsonify({
        "table": table,
        "caslib": CONTROLLED_CASLIB,
        "status": status,
        "insights": insights,
        "llm_explanation": llm_explanation
    })
