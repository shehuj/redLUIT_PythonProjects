import os
import sys
import json
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_REQUIRED_FILES = ['.gitignore', 'README.md']

def load_required_files(script_dir):
    cfg_path = os.path.join(script_dir, '.required-files.yml')
    if os.path.isfile(cfg_path):
        if yaml is None:
            print("Error: PyYAML not installed, but config file exists.")
            sys.exit(1)
        try:
            with open(cfg_path, 'r') as f:
                cfg = yaml.safe_load(f)
            if not isinstance(cfg, dict) or 'required_files' not in cfg:
                raise ValueError("Malformed config")
            rf = cfg['required_files']
            if not isinstance(rf, list) or not all(isinstance(i, str) for i in rf):
                raise ValueError("required_files must be list of strings")
            return rf
        except Exception as e:
            print(json.dumps({
                "required_files": [],
                "present_files": [],
                "missing_files": [],
                "error": str(e)
            }))
            sys.exit(1)
    return DEFAULT_REQUIRED_FILES

def audit_file_check():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    required = load_required_files(script_dir)
    present = []
    missing = []
    for fname in required:
        p = os.path.join(script_dir, fname)
        if os.path.isfile(p):
            present.append(fname)
        else:
            missing.append(fname)
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "required_files": required,
        "present_files": present,
        "missing_files": missing
    }
    success = (len(missing) == 0)
    return success, result

if __name__ == '__main__':
    from datetime import datetime
    success, ctx = audit_file_check()
    print(json.dumps(ctx))
    if not success:
        sys.exit(1)