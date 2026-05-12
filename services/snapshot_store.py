import json
from pathlib import Path

DATA_DIR = Path("data-dump")
DATA_DIR.mkdir(exist_ok=True)

def snapshot_path(caslib, table):
    return DATA_DIR / f"{caslib}__{table}.json"

def snapshot_exists(caslib, table):
    return snapshot_path(caslib, table).exists()

def save_snapshot(caslib, table, payload):
    with open(snapshot_path(caslib, table), "w") as f:
        json.dump(payload, f, indent=2)

def load_snapshot(caslib, table):
    with open(snapshot_path(caslib, table)) as f:
        return json.load(f)