# abt/loader.py

import json
from pathlib import Path

def load_json(path: Path) -> dict:
    """
    Load a JSON file from disk and return parsed content.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)