import os
import pytest
import log
from ls import ls

def test_ls_nonexistent_path_raises(tmp_path):
    log.LOG_FILE = tmp_path / "shell.log"
    os.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        ls(["/__LIL WAYNE__"])


def test_ls_prints_file_path(tmp_path, capsys):
    log.LOG_FILE = tmp_path / "shell.log"
    os.chdir(tmp_path)
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    ls([str(f)])
    out = capsys.readouterr().out.strip()
    assert out == str(f)


def test_ls_lists_directory(tmp_path, capsys):
    log.LOG_FILE = tmp_path / "shell.log"
    os.chdir(tmp_path)
    (tmp_path / "a.txt").write_text("1", encoding="utf-8")
    (tmp_path / "b.txt").write_text("2", encoding="utf-8")
    ls([str(tmp_path)])
    out = capsys.readouterr().out.splitlines()
    assert "a.txt" in out
    assert "b.txt" in out


def test_ls_long_format_for_dir(tmp_path, capsys):
    log.LOG_FILE = tmp_path / "shell.log"
    os.chdir(tmp_path)
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    ls(["-l", str(tmp_path)])
    out = capsys.readouterr().out
    assert "a.txt" in out
    assert "bytes" in out


def test_ls_default_cwd_with_l(tmp_path, capsys):
    log.LOG_FILE = tmp_path / "shell.log"
    os.chdir(tmp_path)
    (tmp_path / "here.txt").write_text("1", encoding="utf-8")
    ls(["-l"])
    out = capsys.readouterr().out
    assert "here.txt" in out
    assert "bytes" in out