import json
from pathlib import Path

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def save_json(data: dict, path: str):
    ensure_dir(str(Path(path).parent))
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

def save_text(content: str, path: str):
    ensure_dir(str(Path(path).parent))
    Path(path).write_text(content, encoding="utf-8")
