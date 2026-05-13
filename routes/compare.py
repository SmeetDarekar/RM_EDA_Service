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
from abt.target_detection import detect_target_column_from_dump
from abt.column_kpi_insights import generate_analyze_column_kpi_insights
from abt.column_kpi_insights import generate_compare_column_kpi_insights

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

# Need to implement it here too
# base_target_info = detect_target_column_from_dump(base_raw["items"])
# compare_target_info = detect_target_column_from_dump(compare_raw["items"])


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




        # We are trying the new KPI comparison here
        column_kpi_insights = generate_compare_column_kpi_insights(
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

    #  EXISTING CONTRACT (RESTORED)
    verdict=kpis["verdict"],
    reasons=kpis.get("reasons", []),

    #  EXISTING OUTPUT
    insights=insights,
    kpis=kpis,
    llm_explanation=llm_explanation,

    #  ADD-ONS (UNCHANGED)
    kpi_summary=kpi_summary,
    column_quality=column_quality,
    column_comparison=column_comparison,
    column_kpi_insights = column_kpi_insights
)

    except Exception as e:
        print("COMPARE FAILED:", str(e))
        return render_template(
            "compare_results.html",
            error=str(e)
        )