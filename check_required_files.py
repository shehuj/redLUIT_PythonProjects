import os
import sys
import json
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_REQUIRED_FILES = [".gitignore", "README.md", "requirements.txt"]


def load_required_files(script_dir):
    cfg_path = os.path.join(script_dir, ".required-files.yml")
    if os.path.isfile(cfg_path):
        if yaml is None:
            print("Error: PyYAML not installed, but config file exists.")
            sys.exit(1)
        try:
            with open(cfg_path, "r") as f:
                cfg = yaml.safe_load(f)
            if not isinstance(cfg, dict) or "required_files" not in cfg:
                raise ValueError(
                    "Malformed config: missing 'required_files' key or not dict."
                )
            rf = cfg["required_files"]
            if not isinstance(rf, list) or not all(isinstance(i, str) for i in rf):
                raise ValueError("'required_files' must be a list of strings.")
            rf_clean = [i.strip() for i in rf]  # Strip whitespace
            return rf_clean
        except Exception as e:
            print(
                json.dumps(
                    {
                        "required_files": [],
                        "present_files": [],
                        "missing_files": [],
                        "error": str(e),
                    }
                )
            )
            sys.exit(1)
    return DEFAULT_REQUIRED_FILES


def audit_file_check():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    required = load_required_files(script_dir)

    present = []
    missing = []
    debug_info = {}

    for fname in required:
        fname_clean = fname.strip()
        p = os.path.join(script_dir, fname_clean)
        exists = os.path.isfile(p)
        debug_info[fname_clean] = {"path_checked": p, "exists": exists}
        if exists:
            present.append(fname_clean)
        else:
            missing.append(fname_clean)

    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "required_files": required,
        "present_files": present,
        "missing_files": missing,
        "debug": debug_info,
    }

    # Exit if any required file is missing
    if missing:
        print(json.dumps(result))
        sys.exit(1)

    print(json.dumps(result))
    return True


if __name__ == "__main__":
    audit_file_check()
