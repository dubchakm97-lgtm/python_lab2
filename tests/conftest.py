from pathlib import Path
import sys
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

@pytest.fixture(autouse=True)
def _setup_env(monkeypatch, tmp_path):
    import log
    monkeypatch.setattr(log, "LOG_FILE", tmp_path / "shell.log")
    monkeypatch.chdir(tmp_path)

@pytest.fixture
def fake_home(monkeypatch, tmp_path):
    import os
    monkeypatch.setattr(os.path, "expanduser", lambda p: str(tmp_path) if p == "~" else p)
    return tmp_path

@pytest.fixture
def fake_input(monkeypatch):
    import builtins
    def _feed(seq):
        it = iter(seq)
        monkeypatch.setattr(builtins, "input", lambda prompt="": next(it))
    return _feed