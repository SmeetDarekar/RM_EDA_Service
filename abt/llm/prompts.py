# # def risk_insight_prompt(insight: dict) -> str:
# #     return f"""
# # You are a senior Risk Analytics and Model Validation expert.

# # You are reviewing findings from an Automated ABT(Analytics BAse Table) Drift Analysis system.

# # Your task:
# # - Explain the finding in clear, professional language
# # - Focus on risk, governance, and modelling implications
# # - DO NOT invent data
# # - DO NOT suggest new analytics
# # - Only explain what is provided

# # === FINDING CONTEXT ===
# # Severity: {insight['severity']}
# # Category: {insight['category']}
# # Dataset Stage: {insight.get('stage')}

# # Observed Behavior:
# # {chr(10).join('- ' + x for x in insight['observed_behavior'])}

# # Detected Pattern:
# # {insight['detected_pattern']}

# # Likely Cause:
# # {insight['likely_cause']}

# # Risk Implications:
# # {chr(10).join('- ' + x for x in insight['risk_implication'])}

# # Recommended Action:
# # {insight['recommended_action']}

# # === OUTPUT FORMAT ===
# # Write a concise explanation (5–8 sentences) suitable for:
# # - Model validation notes
# # - Risk review meetings
# # - Audit documentation
# # """



# def risk_insight_prompt(insight: dict) -> str:
#     visual_obs = insight["evidence"].get("visual_observations", [])

#     return f"""
# You are a senior Risk Analytics and Model Validation expert.

# You are reviewing findings from an Automated ABT Drift Analysis system.
# The system includes diagnostic visualizations such as:
# - distribution overlap plots
# - boxplots across stages
# - tail behavior views
# - missingness heatmaps

# IMPORTANT RULES:
# - Refer explicitly to what is visible in the plots **only if visual observations are provided**
# - Do NOT invent visual behavior
# - Use phrasing like "based on the drift plots" or "the boxplots indicate..."

# === FINDING CONTEXT ===
# Severity: {insight['severity']}
# Category: {insight['category']}
# Dataset Stage: {insight.get('stage')}

# Observed Statistical Behavior:
# {chr(10).join('- ' + x for x in insight['observed_behavior'])}

# Visual Observations from Drift Plots:
# {chr(10).join('- ' + x for x in visual_obs) if visual_obs else '- No significant visual anomalies observed'}

# Detected Pattern:
# {insight['detected_pattern']}

# Likely Cause:
# {insight['likely_cause']}

# Risk Implications:
# {chr(10).join('- ' + x for x in insight['risk_implication'])}

# Recommended Action:
# {insight['recommended_action']}

# === OUTPUT INSTRUCTIONS ===
# Produce a concise, professional explanation (6–10 sentences) that:
# - Explicitly references the drift plots where relevant
# - Explains how the visual evidence supports the conclusion
# - Is suitable for model validation and audit documentation
# """


# llm/prompts.py

def abt_comparison_narration_prompt(
    base_abt: str,
    compare_abt: str,
    insights: list
) -> str:
    """
    Prompt for explaining ABT-level comparison outcomes.
    This is NOT feature drift narration.
    """

    return f"""
You are a senior Risk Modeling and Model Governance reviewer.

You are reviewing a comparison between two Analytics Base Tables (ABTs):

- Base ABT: {base_abt}
- Compared ABT: {compare_abt}

The system has produced the following validated insights:
{insights}

Your task is to:
- Explain what these findings mean in clear, business-oriented language
- Clarify whether the comparison result is blocking or informational
- Distinguish structural issues from data quality or model stability issues
- Clearly state what the user should do next

IMPORTANT RULES:
- Do NOT repeat raw statistics or column counts
- Do NOT invent new findings
- Do NOT speculate beyond the provided insights
- Focus on decision impact, governance clarity, and next steps

OUTPUT REQUIREMENTS:
- Write 1–2 short paragraphs
- Suitable for risk review meetings and audit documentation
"""

# abt/llm/prompts.py

def analyze_abt_prompt(payload: dict) -> str:
    """
    LLM prompt for SINGLE‑ABT analysis narration.
    Produces short, structured, action-oriented output.
    """

    summary = payload.get("summary", {})
    findings = payload.get("findings", [])

    table = summary.get("table", "UNKNOWN")
    total_columns = summary.get("total_columns", "N/A")

    findings_text = "\n".join(
        f"- [{f.get('severity', 'INFO')}] {f.get('message', '')}"
        for f in findings
    )

    return f"""
You are a senior Risk Modeling and Model Validation expert.

You are reviewing automated analysis results for a SINGLE Analytics Base Table (ABT).

ABT Name: {table}
Total Columns: {total_columns}

The system has produced the following validated findings:
{findings_text}

YOUR TASK:
Rewrite the above findings into a SHORT, STRUCTURED summary using the format below.

FORMAT (follow strictly):

🔍 Automated Analysis Summary — {table}

🚦 Overall Readiness:
- Ready / Not Ready for Modeling (choose one)

🟥 Critical Issues (must block modeling):
- Bullet points (only if applicable)

⚠️ Data Quality Concerns:
- Bullet points listing affected columns and why they matter

⚠️ Feature Quality Issues:
- Bullet points (e.g., low variance, non-informative features)

⚠️ Governance / Leakage Risks:
- Bullet points (e.g., identifier-like fields)

✅ What Can Proceed After Fixes:
- Short bullets describing next possible steps

RULES:
- Be concise and structured (no long paragraphs)
- Do NOT invent new findings
- Do NOT repeat raw statistics
- Do NOT speculate
- Use clear, business-oriented language suitable for governance review
STRICT OUTPUT RULES:
- Use bullet points only
- One issue per bullet
- Maximum 7 words per bullet
- No paragraphs
- No explanations longer than one line
- Group bullets under clear section headers
"""