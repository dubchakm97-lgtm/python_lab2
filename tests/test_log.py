import log
import pytest

def test_log_writes_line(tmp_path):
    log.LOG_FILE = tmp_path / "shell.log"
    log.log_message("hello")
    text = log.LOG_FILE.read_text(encoding="utf-8").strip()
    assert text.endswith(" hello")

def test_log_appends(tmp_path):
    log.LOG_FILE = tmp_path / "shell.log"
    log.log_message("one")
    log.log_message("two")
    lines = log.LOG_FILE.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert lines[-1].endswith(" two")

def test_log_utf8(tmp_path):
    log.LOG_FILE = tmp_path / "shell.log"
    log.log_message("привет")
    text = log.LOG_FILE.read_text(encoding="utf-8")
    assert "привет" in text