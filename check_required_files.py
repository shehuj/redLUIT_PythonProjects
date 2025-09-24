import os
import sys

# Default required files if no config is found
DEFAULT_REQUIRED_FILES = ['.gitignore', 'README.md']

def load_required_files():
    """
    If a `.required-files.yml` file exists in the same directory as this script,
    load it and return the list under the `required_files` key.
    Otherwise return DEFAULT_REQUIRED_FILES.
    If malformed, print error and exit.
    """
    try:
        import yaml
    except ImportError:
        yaml = None

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '.required-files.yml')
    if os.path.isfile(config_path):
        if yaml is None:
            print("Error: yaml module not found, but .required-files.yml exists.")
            print("Please install PyYAML (pip install pyyaml).")
            sys.exit(1)
        try:
            with open(config_path, 'r') as f:
                cfg = yaml.safe_load(f)
            if not isinstance(cfg, dict):
                raise ValueError("Configuration file must be a mapping (dictionary).")
            if 'required_files' not in cfg:
                raise ValueError("Configuration missing 'required_files' key.")
            rf = cfg['required_files']
            if not isinstance(rf, list) or not all(isinstance(item, str) for item in rf):
                raise ValueError("'required_files' must be a list of strings.")
            return rf
        except Exception as e:
            print(f"Error reading configuration from {config_path}: {e}")
            sys.exit(1)
    # No config file — use default
    return DEFAULT_REQUIRED_FILES

def check_required_files(required_files):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    missing = []
    for fname in required_files:
        path = os.path.join(script_dir, fname)
        if not os.path.isfile(path):
            missing.append((fname, path))

    if missing:
        print("Error: The following required files are missing (looked in same directory as script):")
        for fname, path in missing:
            print(f" - {fname}, expected at: {path}")
        sys.exit(1)
    
#    else:
#       print("All required files are present at:", script_dir)

if __name__ == '__main__':
    required = load_required_files()
    check_required_files(required)