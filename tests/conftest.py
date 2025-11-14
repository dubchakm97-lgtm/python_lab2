import os
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

@pytest.fixture(autouse=True)
def _isolate_fs_and_log(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    import log
    monkeypatch.setattr(log, "LOG_FILE", tmp_path / "shell.log")

@pytest.fixture
def fake_home(monkeypatch, tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(os.path, "expanduser", lambda p: str(home) if p == "~" else p)
    return home

@pytest.fixture
def fake_input(monkeypatch):
    import builtins
    def _feed(seq):
        it = iter(seq)
        monkeypatch.setattr(builtins, "input", lambda prompt="": next(it))
    return _feed