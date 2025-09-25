import os
import sys
import json
import yaml
import pytest

# Ensure script directory is on import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from check_required_files import load_required_files, audit_file_check

@pytest.fixture(autouse=True)
def restore_cwd(tmp_path, monkeypatch):
    """
    Fixture to run tests in isolated temporary directory and restore cwd.
    It yields the tmp_path, and resets cwd after test.
    """
    orig = os.getcwd()
    monkeypatch.chdir(tmp_path)
    yield tmp_path
    monkeypatch.chdir(orig)

def write_files(base_dir, filenames):
    for fname in filenames:
        (base_dir / fname).write_text("")

def test_with_custom_required_files(monkeypatch):
    # Create a .required-files.yml that only requires two files
    custom = { "required_files": ["A.txt", "B.txt"] }
    (os.getcwd() / ".required-files.yml").write_text(yaml.dump(custom))
    # Create only A.txt
    write_files(os.getcwd(), ["A.txt"])
    # Do not create B.txt
    success, ctx = audit_file_check()
    assert success is False
    assert ctx["required_files"] == ["A.txt", "B.txt"]
    assert "A.txt" in ctx["present_files"]
    assert "B.txt" in ctx["missing_files"]

def test_custom_all_present(monkeypatch):
    custom = { "required_files": ["X", "Y"] }
    (os.getcwd() / ".required-files.yml").write_text(yaml.dump(custom))
    write_files(os.getcwd(), ["X", "Y"])
    success, ctx = audit_file_check()
    assert success is True
    assert ctx["missing_files"] == []

def test_no_config_falls_back_to_default(monkeypatch):
    # No config file created
    # Create only a subset of default required files
    # But for success test, we should create *all* of defaults
    from check_required_files import DEFAULT_REQUIRED_FILES
    write_files(os.getcwd(), DEFAULT_REQUIRED_FILES)
    success, ctx = audit_file_check()
    assert success is True
    assert ctx["missing_files"] == []

def test_no_config_missing_default(monkeypatch):
    # No config, but missing at least one default required file
    from check_required_files import DEFAULT_REQUIRED_FILES
    present = DEFAULT_REQUIRED_FILES[:-1]  # all except last
    write_files(os.getcwd(), present)
    success, ctx = audit_file_check()
    assert success is False
    # The one missing should be detected
    assert len(ctx["missing_files"]) == 1
    missing = ctx["missing_files"][0]
    assert missing not in ctx["present_files"]
    assert missing in DEFAULT_REQUIRED_FILES