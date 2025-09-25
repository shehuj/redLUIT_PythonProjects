import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from unittest.mock import patch
from check_required_files import load_required_files, audit_file_check

# Check all required files are present
@patch("os.path.isfile")
def test_all_files_present(mock_isfile):
    # Simulate that all required files exist
    mock_isfile.side_effect = lambda fname: fname in [
        ".gitignore",
        "README.md",
        "requirements.txt",
    ]
    success, result = audit_file_check()
    assert success
    assert not result["missing_files"]