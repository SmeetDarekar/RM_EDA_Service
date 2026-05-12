# services/ic_client.py

import requests
from typing import Optional, Dict, Any

BASE_URL = "https://<BASE_URL>"
IC_INSTANCES_ENDPOINT = f"{BASE_URL}/catalog/instances"

ACCESS_TOKEN="YOUR ACCESS TOEKN"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}


def fetch_table_metadata(
    *,
    table_name: str,
    caslib: Optional[str] = None,
    limit: int = 3000
) -> Optional[Dict[str, Any]]:
    """
    Fetch IC metadata for a CAS table using /catalog/instances.

    IMPORTANT:
    - table_name MUST always be provided explicitly (keyword-only)
    - caslib is optional (analyze flow vs compare flow)
    """

    if caslib:
        filter_expr = (
            "and("
            f"eq(caslib,'{caslib}'),"
            f"contains(resourceId,'{table_name}'),"
            "eq(definition,'casColumn')"
            ")"
        )
    else:
        # Analyze flow: single controlled CASLIB
        filter_expr = (
            "and("
            f"contains(resourceId,'{table_name}'),"
            "eq(definition,'casColumn')"
            ")"
        )

    params = {
        "filter": filter_expr,
        "level": "detailedMetrics",
        "limit": limit
    }

    response = requests.get(
        IC_INSTANCES_ENDPOINT,
        headers=HEADERS,
        params=params,
        verify=False,
        timeout=30
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    payload = response.json()
    if not payload.get("items"):
        return None

    return payload
