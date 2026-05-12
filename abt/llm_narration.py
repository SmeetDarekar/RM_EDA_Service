# abt/llm_narration.py

def build_llm_narration_prompt(base_table, compare_table, insights):
    """
    Converts deterministic insights into a business-facing explanation.
    """

    return f"""
You are a Risk Modeling Reviewer.

You are reviewing a comparison between two ABTs:
- Base ABT: {base_table}
- Compared ABT: {compare_table}

Below are system-detected insights:
{insights}

Your task:
- Explain what these findings mean in plain business language
- Clarify whether this comparison is blocking or informational
- Clearly state what the user should do next

Rules:
- Do NOT repeat raw statistics
- Do NOT speculate beyond provided insights
- Focus on decision impact and governance clarity
"""
