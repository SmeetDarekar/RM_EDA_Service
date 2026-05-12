# # services/ic_client.py

# import requests
# from typing import Optional, Dict, Any

# # ------------------------------------------------------------------
# # Configuration (keep these configurable / injectable later)
# # ------------------------------------------------------------------

# BASE_URL = "https://d116403.ingress-nginx.rci1322a-m1.tsr-rci-ciaws.hpos.rnd.sas.com"
# IC_INSTANCES_ENDPOINT = f"{BASE_URL}/catalog/instances"

# ACCESS_TOKEN = "eyJqa3UiOiJodHRwczovL2xvY2FsaG9zdC9TQVNMb2dvbi90b2tlbl9rZXlzIiwia2lkIjoibGVnYWN5LXRva2VuLWtleSIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzODhmYzk1ZS03Y2VkLTQ3NDEtYmI5NS0xZTdmNDdlYTNiZjMiLCJzZXNzaW9uX3NpZyI6IjdiOWM1NWM4LTVmMzEtNGVlZS04ZGUwLWU4OGNhNjY0YWE0YyIsInVzZXJfbmFtZSI6InNhc2FkbSIsIm9yaWdpbiI6ImxkYXAiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L1NBU0xvZ29uL29hdXRoL3Rva2VuIiwiYXV0aG9yaXRpZXMiOlsiUk1BZG1pbnMiLCJDaXJydXNBZG1pbnMiLCJyaXNrTW9kZWxpbmdBcHBBZG1pbiIsIlJNTW9kZWxlcnMiLCJyaXNrRGF0YUFkbWluIiwicmlza01vZGVsZXIiLCJyaXNrRGF0YUFuYWx5c3QiLCJyaXNrRGF0YUNvbmZpZ1VzZXJzIiwicmlza01vZGVsVmFsaWRhdG9yIiwiQ2lycnVzQnVpbGRlclNvbHV0aW9uVXNlcnMiLCJSTVZhbGlkYXRvcnMiLCJDaXJydXNVc2VycyIsIlJNRGF0YU1hbmFnZXJzIl0sImNsaWVudF9pZCI6Im15Y2xpZW50aWQiLCJhdWQiOlsibXljbGllbnRpZCIsInVhYSIsIm9wZW5pZCJdLCJleHRfaWQiOiJ1aWQ9c2FzYWRtLG91PXVzZXJzLGRjPWdlbCxkYz1jb20iLCJyZW1vdGVfaXAiOiIxNzIuMjYuODYuMjU0IiwiemlkIjoidWFhIiwiZ3JhbnRfdHlwZSI6ImF1dGhvcml6YXRpb25fY29kZSIsInVzZXJfaWQiOiIzODhmYzk1ZS03Y2VkLTQ3NDEtYmI5NS0xZTdmNDdlYTNiZjMiLCJhenAiOiJteWNsaWVudGlkIiwic2NvcGUiOlsib3BlbmlkIiwidWFhLnVzZXIiXSwiYXV0aF90aW1lIjoxNzc4MDYwNDM3LCJleHAiOjE3NzgwNjQwMzgsImlhdCI6MTc3ODA2MDQzOCwianRpIjoiYzg2YWQ5ZmFlNjdmNDkxZWFhMzcwODJmMjVmZTAyNDgiLCJlbWFpbCI6InNhc2FkbUBnZWwuY29tIiwicmV2X3NpZyI6ImRlZmNlZWRkIiwiY2lkIjoibXljbGllbnRpZCJ9.B8EJRtctQfxofh2t1yaMc65uJa4urrRgqfkzeV8ygr5d_ChniDFN7UPicisu8fSP_zibtxB1UiJ0CWebhrH1RNJrFuz91ABTUSVzbgZbizQmZujvzF5TwsmMJh5M_iPVzRzyrMMYG7LwZF8eZ1G1yxkTzrs00zo0BRdZLbCgy2j3mTeKPMYBxl5j7-tM51hEQBfDf5_YUFmFHG9lgcD6MsL9OamADEwf9YRWs9ypTHgPIYEUMmz5rhIBP-SpaggoR0F81MnZK8Aq8qE4AbBTRypytKdcf4hH6CEld4s4Q04lWS23wGcQGV8M_ztaugyuZFONRYRGIid-L1rYt_nS0w"   # TODO: inject via env / auth module


# HEADERS = {
#     "Authorization": f"Bearer {ACCESS_TOKEN}",
#     "Accept": "application/json"  # ✅ correct for collection endpoints
# }


# # ------------------------------------------------------------------
# # IC metadata fetch
# # ------------------------------------------------------------------

# def fetch_table_metadata(
#     table_name: str,
#     caslib: Optional[str] = None,
#     limit: int = 3000
# ) -> Optional[Dict[str, Any]]:
#     """
#     Fetch column-level metadata and statistics for a CAS table
#     using SAS Information Catalog (/catalog/instances).

#     Parameters
#     ----------
#     table_name : str
#         CAS table name (required)

#     caslib : str | None
#         CASLIB name (optional; can be skipped if you operate on a
#         single controlled CASLIB and rely on resourceId matching)

#     limit : int
#         Max number of instances to return

#     Returns
#     -------
#     dict | None
#         IC response JSON if table is found, else None
#     """

#     # --------------------------------------------------------------
#     # Build IC filter (this matches your *working* code)
#     # --------------------------------------------------------------

#     if caslib:
#         filter_expr = (
#             "and("
#             f"eq(caslib,'{caslib}'),"
#             f"contains(resourceId,'{table_name}'),"
#             "eq(definition,'casColumn')"
#             ")"
#         )
#     else:
#         # ✅ Analyze flow: caslib is implicit (controlled zone)
#         filter_expr = (
#             "and("
#             f"contains(resourceId,'{table_name}'),"
#             "eq(definition,'casColumn')"
#             ")"
#         )

#     params = {
#         "filter": filter_expr,
#         "level": "detailedMetrics",
#         "limit": limit
#     }

#     # --------------------------------------------------------------
#     # Call IC
#     # --------------------------------------------------------------

#     response = requests.get(
#         IC_INSTANCES_ENDPOINT,
#         headers=HEADERS,
#         params=params,
#         verify=False,
#         timeout=30
#     )

#     # --------------------------------------------------------------
#     # Error handling
#     # --------------------------------------------------------------

#     if response.status_code == 404:
#         return None

#     response.raise_for_status()

#     payload = response.json()

#     # No matching instances → table not found / not discovered
#     if not payload.get("items"):
#         return None

#     return payload









# services/ic_client.py

import requests
from typing import Optional, Dict, Any

BASE_URL = "https://d116403.ingress-nginx.rci1322a-m1.tsr-rci-ciaws.hpos.rnd.sas.com"
IC_INSTANCES_ENDPOINT = f"{BASE_URL}/catalog/instances"

ACCESS_TOKEN="eyJqa3UiOiJodHRwczovL2xvY2FsaG9zdC9TQVNMb2dvbi90b2tlbl9rZXlzIiwia2lkIjoibGVnYWN5LXRva2VuLWtleSIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzODhmYzk1ZS03Y2VkLTQ3NDEtYmI5NS0xZTdmNDdlYTNiZjMiLCJzZXNzaW9uX3NpZyI6IjJlNGIzZWI3LTA2YjEtNDdhMC04OGVmLTE5NDE3ZDk3ZGVmMSIsInVzZXJfbmFtZSI6InNhc2FkbSIsIm9yaWdpbiI6ImxkYXAiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L1NBU0xvZ29uL29hdXRoL3Rva2VuIiwiYXV0aG9yaXRpZXMiOlsiUk1BZG1pbnMiLCJDaXJydXNBZG1pbnMiLCJyaXNrTW9kZWxpbmdBcHBBZG1pbiIsIlJNTW9kZWxlcnMiLCJyaXNrRGF0YUFkbWluIiwicmlza01vZGVsZXIiLCJyaXNrRGF0YUFuYWx5c3QiLCJyaXNrRGF0YUNvbmZpZ1VzZXJzIiwicmlza01vZGVsVmFsaWRhdG9yIiwiQ2lycnVzQnVpbGRlclNvbHV0aW9uVXNlcnMiLCJSTVZhbGlkYXRvcnMiLCJDaXJydXNVc2VycyIsIlJNRGF0YU1hbmFnZXJzIl0sImNsaWVudF9pZCI6Im15Y2xpZW50aWQiLCJhdWQiOlsibXljbGllbnRpZCIsInVhYSIsIm9wZW5pZCJdLCJleHRfaWQiOiJ1aWQ9c2FzYWRtLG91PXVzZXJzLGRjPWdlbCxkYz1jb20iLCJyZW1vdGVfaXAiOiIxNzIuMjYuMTY0LjQzIiwiemlkIjoidWFhIiwiZ3JhbnRfdHlwZSI6ImF1dGhvcml6YXRpb25fY29kZSIsInVzZXJfaWQiOiIzODhmYzk1ZS03Y2VkLTQ3NDEtYmI5NS0xZTdmNDdlYTNiZjMiLCJhenAiOiJteWNsaWVudGlkIiwic2NvcGUiOlsib3BlbmlkIiwidWFhLnVzZXIiXSwiYXV0aF90aW1lIjoxNzc4NDkzMTYyLCJleHAiOjE3Nzg0OTY3NjIsImlhdCI6MTc3ODQ5MzE2MiwianRpIjoiMjkxMzlhOTY0MTVlNDg3NGFhODNjMmY2YzAzYjNkZDAiLCJlbWFpbCI6InNhc2FkbUBnZWwuY29tIiwicmV2X3NpZyI6ImRlZmNlZWRkIiwiY2lkIjoibXljbGllbnRpZCJ9.T5OxsZaGBE7bOtOq50QnKrVvxjBoeCdVHal_pdnGN6F8vsGteRk71QMNBFhNQl5DfOouDQMaGUMsd_nsiZOU08qwFi2vVq4yuOz9JRxDtYYMrHEGRZLdkpCUxqAGJ7g2ZOJ3LQQU9axvZttPispmHEi-r_Ds8rPjaZqK9B06MJ79lVC9JdX5C0ZgIcpmLwyV-9ebWBDEdhY3gkHYbgoUU7AAvPJis6TLAq7_16qMKNN0qDeqRA_8tUxB-0Hr1oN7IOH5EbpE5sOoFw3MYQsk_2QqmrwKG7IH3HMp7g2SqVwAEzPRuLCFWG7xYywCEmWuQrKcBBhWJkkRG8knV5jihw"

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