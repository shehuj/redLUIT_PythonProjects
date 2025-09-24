# Check required files exist in the root directory
import os
import sys

required_files = (
    '.gitignore',
    'README.md',
    'requirements.txt'
)

os.path.abspath(__file__) # Get absolute path of the current script

def check_required_files():
# Current Directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Check for required files
    missing_files = []
    for fname in required_files:
        path = os.path.join(script_dir, fname)
        if not os.path.isfile(path):
            missing_files.append(fname)

# Report missing files and exit with error
    if missing_files:
        print("Error: The following required files are missing:")
        for f in missing_files:
            print(f" - {f}")
        sys.exit(1)

# All required files are present
if __name__ == '__main__':
    check_required_files()