# # routes/compare.py

# from flask import Blueprint, request, render_template, jsonify

# from services.snapshot_store import (
#     load_snapshot,
#     snapshot_exists
# )
# from services.ic_client import fetch_table_metadata
# from abt.snapshot import ABTSnapshot
# from abt.comparator import ABTComparator

# compare_bp = Blueprint("compare", __name__)


# # ------------------------------------------------------------------
# # Input extraction (UI + API)
# # ------------------------------------------------------------------

# def _get_compare_inputs():
#     """
#     Supports both:
#     1) UI form submission
#     2) JSON API requests
#     """

#     if request.form:
#         return (
#             request.form.get("base_caslib"),
#             request.form.get("base_table"),
#             request.form.get("compare_caslib"),
#             request.form.get("compare_table"),
#         )

#     payload = request.get_json(silent=True) or {}

#     base = payload.get("base", {})
#     compare = payload.get("compare", {})

#     return (
#         base.get("caslib"),
#         base.get("table"),
#         compare.get("caslib"),
#         compare.get("table"),
#     )


# # ------------------------------------------------------------------
# # Compare endpoint
# # ------------------------------------------------------------------

# @compare_bp.route("/compare", methods=["POST"])
# def compare():
#     (
#         base_caslib,
#         base_table,
#         compare_caslib,
#         compare_table,
#     ) = _get_compare_inputs()


#     if request.form:
#         # give immediate feedback
#         from flask import render_template
#         return render_template("compare_loading.html")

#     # --------------------------------------------------------------
#     # 1. Validate inputs
#     # --------------------------------------------------------------
#     if not all([base_caslib, base_table, compare_caslib, compare_table]):
#         msg = "Base and compare CASLIB + table names are required"
#         if request.form:
#             return render_template("compare.html", error=msg)
#         return jsonify({"error": msg}), 400

#     # --------------------------------------------------------------
#     # 2. Ensure base snapshot exists (or create it)
#     # --------------------------------------------------------------
#     if not snapshot_exists(base_caslib, base_table):
#         raw = fetch_table_metadata(
#             table_name=base_table,
#             caslib=base_caslib
#         )
#         if raw is None:
#             msg = f"Base table {base_caslib}.{base_table} not found in Information Catalog"
#             if request.form:
#                 return render_template("compare.html", error=msg)
#             return jsonify({"error": msg}), 404

#         # Persist snapshot
#         from services.snapshot_store import save_snapshot
#         save_snapshot(base_caslib, base_table, raw)

#     # --------------------------------------------------------------
#     # 3. Ensure compare snapshot exists (or create it)
#     # --------------------------------------------------------------
#     if not snapshot_exists(compare_caslib, compare_table):
#         raw = fetch_table_metadata(
#             table_name=compare_table,
#             caslib=compare_caslib
#         )
#         if raw is None:
#             msg = f"Compare table {compare_caslib}.{compare_table} not found in Information Catalog"
#             if request.form:
#                 return render_template("compare.html", error=msg)
#             return jsonify({"error": msg}), 404

#         from services.snapshot_store import save_snapshot
#         save_snapshot(compare_caslib, compare_table, raw)

#     # --------------------------------------------------------------
#     # 4. Load snapshots
#     # --------------------------------------------------------------
#     base_raw = load_snapshot(base_caslib, base_table)
#     compare_raw = load_snapshot(compare_caslib, compare_table)

#     abt_base = ABTSnapshot(
#         name=base_table,
#         stage="BASE",
#         fetched_at=base_raw.get("analysisTimeStamp") or base_raw.get("fetchedAt"),
#         raw_items=base_raw["items"],
#     )

#     abt_compare = ABTSnapshot(
#         name=compare_table,
#         stage="COMPARE",
#         fetched_at=compare_raw.get("analysisTimeStamp") or compare_raw.get("fetchedAt"),
#         raw_items=compare_raw["items"],
#     )

#     # --------------------------------------------------------------
#     # 5. Run comparison logic
#     # --------------------------------------------------------------
#     comparator = ABTComparator(abt_base, abt_compare)

#     results = {
#         "base": f"{base_caslib}.{base_table}",
#         "compare": f"{compare_caslib}.{compare_table}",
#         "missing_columns": comparator.missing_columns(),
#         "additional_columns": comparator.additional_columns(),
#         "stat_differences": comparator.compare_stats(),
#         "completeness_rating": comparator.completeness_score(),
#     }

#     # --------------------------------------------------------------
#     # 6. Return response (UI or API)
#     # --------------------------------------------------------------
#     if request.form:
#         return render_template(
#             "compare.html",
#             results=results
#         )

#     return jsonify(results)
















#routes/compare.py# flask import Blueprint, request, render_template, jsonify

# from flask import Blueprint, render_template, request

# from abt.abt_kpi_engine import compute_abt_level_kpis


# from services.snapshot_store import (
#     load_snapshot,
#     snapshot_exists,
#     save_snapshot
# )
# from services.ic_client import fetch_table_metadata
# from abt.snapshot import ABTSnapshot
# from abt.comparator import ABTComparator

# compare_bp = Blueprint("compare", __name__)

# # --------------------------------------------------
# # STEP 1: FAST ROUTE – show status immediately
# # --------------------------------------------------
# @compare_bp.route("/compare", methods=["POST"])
# def compare_start():
#     base_caslib = request.form.get("base_caslib")
#     base_table = request.form.get("base_table")
#     compare_caslib = request.form.get("compare_caslib")
#     compare_table = request.form.get("compare_table")

#     if not all([base_caslib, base_table, compare_caslib, compare_table]):
#         return render_template(
#             "compare.html",
#             error="All fields are required for comparison"
#         )

#     # Immediate UI feedback
#     return render_template(
#         "compare_loading.html",
#         base_caslib=base_caslib,
#         base_table=base_table,
#         compare_caslib=compare_caslib,
#         compare_table=compare_table
#     )


# # --------------------------------------------------
# # STEP 2: SLOW ROUTE – real work happens here
# # --------------------------------------------------
# @compare_bp.route("/compare/run", methods=["POST"])
# def compare_run():
#     base_caslib = request.form.get("base_caslib")
#     base_table = request.form.get("base_table")
#     compare_caslib = request.form.get("compare_caslib")
#     compare_table = request.form.get("compare_table")

#     try:
#         print("==== COMPARE START ====")

#         # -----------------------------
#         # Snapshot existence checks
#         # -----------------------------
#         print("Checking snapshot for base table:", base_table)
#         base_exists = snapshot_exists(base_caslib, base_table)
#         print("Base snapshot exists:", base_exists)

#         print("Checking snapshot for compare table:", compare_table)
#         compare_exists = snapshot_exists(compare_caslib, compare_table)
#         print("Compare snapshot exists:", compare_exists)

#         # -----------------------------
#         # Fetch from IC if required
#         # -----------------------------
#         if not base_exists:
#             print(f"Fetching IC metadata for BASE table: {base_table}")
#             raw = fetch_table_metadata(table_name=base_table)
#             if raw is None:
#                 raise ValueError(f"Base table {base_table} not found in Information Catalog")
#             save_snapshot(base_caslib, base_table, raw)
#             print("Base snapshot saved")

#         if not compare_exists:
#             print(f"Fetching IC metadata for COMPARE table: {compare_table}")
#             raw = fetch_table_metadata(table_name=compare_table)
#             if raw is None:
#                 raise ValueError(f"Compare table {compare_table} not found in Information Catalog")
#             save_snapshot(compare_caslib, compare_table, raw)
#             print("Compare snapshot saved")

#         # -----------------------------
#         # Load snapshots
#         # -----------------------------
#         print("Loading snapshots from data-dump")
#         base_raw = load_snapshot(base_caslib, base_table)
#         compare_raw = load_snapshot(compare_caslib, compare_table)

#         # -----------------------------
#         # Build ABT snapshots
#         # -----------------------------
#         print("Building ABTSnapshot objects")
#         abt_base = ABTSnapshot(
#             name=base_table,
#             stage="BASE",
#             fetched_at=base_raw.get("fetchedAt"),
#             raw_items=base_raw["items"]
#         )

#         abt_compare = ABTSnapshot(
#             name=compare_table,
#             stage="COMPARE",
#             fetched_at=compare_raw.get("fetchedAt"),
#             raw_items=compare_raw["items"]
#         )

#         # -----------------------------
#         # Run comparison (2-table only)
#         # -----------------------------
#         print("Running ABT comparison logic")
#         comparator = ABTComparator(abt_base, abt_compare)

#         results = {
#             "base": f"{base_caslib}.{base_table}",
#             "compare": f"{compare_caslib}.{compare_table}",
#             "missing_columns": comparator.missing_columns(),
#             "additional_columns": comparator.additional_columns(),
#             "stat_differences": comparator.compare_stats(),
#             "completeness_rating": comparator.completeness_score()
#         }

#         print("==== COMPARE COMPLETE ====")
#         kpis = compute_abt_level_kpis(abt_base, abt_compare)

#         return render_template(
#             "compare_results.html",
#             kpis=kpis,
#             base=f"{base_caslib}.{base_table}",
#             compare=f"{compare_caslib}.{compare_table}"
#         )

#     except Exception as e:
#         print("COMPARE FAILED:", str(e))
#         return render_template(
#             "compare_results.html",
#             error=str(e)
#         )




















# routes/compare.py

# from flask import Blueprint, render_template, request


# from services.snapshot_store import (
#     load_snapshot,
#     snapshot_exists,
#     save_snapshot
# )
# from services.ic_client import fetch_table_metadata

# from abt.snapshot import ABTSnapshot
# from abt.comparator import ABTComparator
# from abt.abt_kpi_engine import compute_abt_level_kpis
# from abt.comparison_interpreter import interpret_comparison
# from abt.llm_narration import build_llm_narration_prompt

# compare_bp = Blueprint("compare", __name__)

# # --------------------------------------------------
# # STEP 1: FAST ROUTE – immediate UI feedback
# # --------------------------------------------------
# @compare_bp.route("/compare", methods=["POST"])
# def compare_start():
#     base_caslib = request.form.get("base_caslib")
#     base_table = request.form.get("base_table")
#     compare_caslib = request.form.get("compare_caslib")
#     compare_table = request.form.get("compare_table")

#     if not all([base_caslib, base_table, compare_caslib, compare_table]):
#         return render_template(
#             "compare.html",
#             error="All fields are required for comparison"
#         )

#     return render_template(
#         "compare_loading.html",
#         base_caslib=base_caslib,
#         base_table=base_table,
#         compare_caslib=compare_caslib,
#         compare_table=compare_table
#     )


# # --------------------------------------------------
# # STEP 2: SLOW ROUTE – full comparison
# # --------------------------------------------------
# @compare_bp.route("/compare/run", methods=["POST"])
# def compare_run():
#     base_caslib = request.form.get("base_caslib")
#     base_table = request.form.get("base_table")
#     compare_caslib = request.form.get("compare_caslib")
#     compare_table = request.form.get("compare_table")

#     try:
#         print("==== COMPARE START ====")

#         # --------------------------------------------------
#         # Snapshot existence checks
#         # --------------------------------------------------
#         if not snapshot_exists(base_caslib, base_table):
#             raw = fetch_table_metadata(table_name=base_table)
#             if raw is None:
#                 raise ValueError(f"Base table {base_table} not found in IC")
#             save_snapshot(base_caslib, base_table, raw)

#         if not snapshot_exists(compare_caslib, compare_table):
#             raw = fetch_table_metadata(table_name=compare_table)
#             if raw is None:
#                 raise ValueError(f"Compare table {compare_table} not found in IC")
#             save_snapshot(compare_caslib, compare_table, raw)

#         # --------------------------------------------------
#         # Load raw snapshots
#         # --------------------------------------------------
#         base_raw = load_snapshot(base_caslib, base_table)
#         compare_raw = load_snapshot(compare_caslib, compare_table)

#         # --------------------------------------------------
#         # ✅ Build ABTSnapshot objects (AUTHORITATIVE)
#         # --------------------------------------------------
#         abt_base = ABTSnapshot(
#             name=base_table,
#             stage="BASE",
#             fetched_at=base_raw.get("fetchedAt"),
#             raw_items=base_raw["items"]
#         )

#         abt_compare = ABTSnapshot(
#             name=compare_table,
#             stage="COMPARE",
#             fetched_at=compare_raw.get("fetchedAt"),
#             raw_items=compare_raw["items"]
#         )

#         # ✅ SANITY CHECK (debug-safe, optional)
#         print("Base ABT columns:", len(abt_base.columns))
#         print("Compare ABT columns:", len(abt_compare.columns))

#         # --------------------------------------------------
#         # Structural + statistical comparison (existing)
#         # --------------------------------------------------
#         comparator = ABTComparator(abt_base, abt_compare)

#         structural_results = {
#             "missing_columns": comparator.missing_columns(),
#             "additional_columns": comparator.additional_columns(),
#             "completeness_rating": comparator.completeness_score(),
#         }

#         # --------------------------------------------------
#         # ✅ Compute ABT-level KPIs (single source of truth)
#         # --------------------------------------------------
#         kpis = compute_abt_level_kpis(abt_base, abt_compare)

#         # --------------------------------------------------
#         # ✅ NEW: Interpretation layer (NO raw ABT access)
#         # --------------------------------------------------
#         insights = interpret_comparison(kpis)

#         # --------------------------------------------------
#         # ✅ NEW: LLM narration prompt (explanatory only)
#         # --------------------------------------------------
#         narration_prompt = build_llm_narration_prompt(
#             base_table=f"{base_caslib}.{base_table}",
#             compare_table=f"{compare_caslib}.{compare_table}",
#             insights=insights
#         )

#         print("==== COMPARE COMPLETE ====")

#         return render_template(
#             "compare_results.html",
#             base=f"{base_caslib}.{base_table}",
#             compare=f"{compare_caslib}.{compare_table}",
#             kpis=kpis,
#             structural=structural_results,
#             insights=insights,
#             narration_prompt=narration_prompt
#         )

#     except Exception as e:
#         print("COMPARE FAILED:", str(e))
#         return render_template(
#             "compare_results.html",
#             error=str(e)
#         )















# routes/compare.py

from flask import Blueprint, render_template, request

from services.snapshot_store import (
    load_snapshot,
    snapshot_exists,
    save_snapshot
)
from services.ic_client import fetch_table_metadata

from abt.snapshot import ABTSnapshot
from abt.comparator import ABTComparator
from abt.abt_kpi_engine import compute_abt_level_kpis
from abt.comparison_interpreter import interpret_comparison

from abt.llm.ollama_client import call_ollama
from abt.llm.prompts import abt_comparison_narration_prompt



from abt.column_level_comparison_view import build_column_level_comparison



from abt.compare_kpi_addon import (
    build_kpi_comparison_summary,
    build_column_level_quality
)


compare_bp = Blueprint("compare", __name__)

# --------------------------------------------------
# STEP 1: FAST ROUTE – immediate UI feedback
# --------------------------------------------------
@compare_bp.route("/compare", methods=["POST"])
def compare_start():
    base_caslib = request.form.get("base_caslib")
    base_table = request.form.get("base_table")
    compare_caslib = request.form.get("compare_caslib")
    compare_table = request.form.get("compare_table")

    if not all([base_caslib, base_table, compare_caslib, compare_table]):
        return render_template(
            "compare.html",
            error="All fields are required for comparison"
        )

    return render_template(
        "compare_loading.html",
        base_caslib=base_caslib,
        base_table=base_table,
        compare_caslib=compare_caslib,
        compare_table=compare_table
    )


# --------------------------------------------------
# STEP 2: SLOW ROUTE – full comparison
# --------------------------------------------------
@compare_bp.route("/compare/run", methods=["POST"])
def compare_run():
    base_caslib = request.form.get("base_caslib")
    base_table = request.form.get("base_table")
    compare_caslib = request.form.get("compare_caslib")
    compare_table = request.form.get("compare_table")

    try:
        print("==== COMPARE START ====")

        # --------------------------------------------------
        # Snapshot existence checks
        # --------------------------------------------------
        if not snapshot_exists(base_caslib, base_table):
            raw = fetch_table_metadata(table_name=base_table)
            if raw is None:
                raise ValueError(f"Base table {base_table} not found in IC")
            save_snapshot(base_caslib, base_table, raw)

        if not snapshot_exists(compare_caslib, compare_table):
            raw = fetch_table_metadata(table_name=compare_table)
            if raw is None:
                raise ValueError(f"Compare table {compare_table} not found in IC")
            save_snapshot(compare_caslib, compare_table, raw)

        # --------------------------------------------------
        # Load raw snapshots
        # --------------------------------------------------
        base_raw = load_snapshot(base_caslib, base_table)
        compare_raw = load_snapshot(compare_caslib, compare_table)

        # --------------------------------------------------
        # Build ABTSnapshot objects (AUTHORITATIVE)
        # --------------------------------------------------
        abt_base = ABTSnapshot(
            name=base_table,
            stage="BASE",
            fetched_at=base_raw.get("fetchedAt"),
            raw_items=base_raw["items"]
        )

        abt_compare = ABTSnapshot(
            name=compare_table,
            stage="COMPARE",
            fetched_at=compare_raw.get("fetchedAt"),
            raw_items=compare_raw["items"]
        )

        print("Base ABT columns:", len(abt_base.columns))
        print("Compare ABT columns:", len(abt_compare.columns))

        # --------------------------------------------------
        # Structural comparison
        # --------------------------------------------------
        comparator = ABTComparator(abt_base, abt_compare)

        structural_results = {
            "missing_columns": comparator.missing_columns(),
            "additional_columns": comparator.additional_columns(),
            "completeness_rating": comparator.completeness_score(),
        }

        # --------------------------------------------------
        # Compute ABT-level KPIs (single source of truth)
        # --------------------------------------------------
        kpis = compute_abt_level_kpis(abt_base, abt_compare)

        # --------------------------------------------------
        # Interpretation layer (decision semantics)
        # --------------------------------------------------
        insights = interpret_comparison(kpis)




        # --------------------------------------------------
# ADD-ON UI DATA (NO LOGIC CHANGE)
# --------------------------------------------------

        base_cols = set(abt_base.columns.keys())
        compare_cols = set(abt_compare.columns.keys())
        missing_columns = sorted(base_cols - compare_cols)

        kpi_summary = build_kpi_comparison_summary(
            missing_columns=missing_columns,
            kpis=kpis
        )

        column_quality = build_column_level_quality(
            base_snapshot=abt_base,
            compare_snapshot=abt_compare
        )

        # --------------------------------------------------
# ADD-ON: Column-Level Comparison (Authoritative IC)
# --------------------------------------------------

        column_comparison = build_column_level_comparison(
            base_snapshot=abt_base,
            compare_snapshot=abt_compare
        )

        # --------------------------------------------------
        # LLM narration (business explanation)
        # --------------------------------------------------
        llm_prompt = abt_comparison_narration_prompt(
            base_abt=f"{base_caslib}.{base_table}",
            compare_abt=f"{compare_caslib}.{compare_table}",
            insights=insights
        )

        try:
            llm_explanation = call_ollama(llm_prompt)
        except Exception as e:
            print("LLM narration failed:", str(e))
            llm_explanation = (
                "Automated explanation could not be generated. "
                "Please review the insights above."
            )

        print("==== COMPARE COMPLETE ====")

        return render_template(
        "compare_results.html",
    base=f"{base_caslib}.{base_table}",
    compare=f"{compare_caslib}.{compare_table}",

    # ✅ EXISTING CONTRACT (RESTORED)
    verdict=kpis["verdict"],
    reasons=kpis.get("reasons", []),

    # ✅ EXISTING OUTPUT
    insights=insights,
    kpis=kpis,
    llm_explanation=llm_explanation,

    # ✅ ADD-ONS (UNCHANGED)
    kpi_summary=kpi_summary,
    column_quality=column_quality,
    column_comparison=column_comparison
)

    except Exception as e:
        print("COMPARE FAILED:", str(e))
        return render_template(
            "compare_results.html",
            error=str(e)
        )