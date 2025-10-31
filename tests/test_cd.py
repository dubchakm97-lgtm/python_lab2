import os
from pathlib import Path
import pytest
from cd import cd

def test_cd_no_args_goes_home(fake_home, capsys):
    cd([])
    out = capsys.readouterr().out
    assert Path(os.getcwd()) == fake_home
    assert "Текущая директория:" in out


def test_cd_into_existing_directory(tmp_path, capsys):
    d = tmp_path / "work"
    d.mkdir()
    cd([str(d)])
    out = capsys.readouterr().out
    assert Path(os.getcwd()) == d
    assert "Текущая директория:" in out


def test_cd_nonexistent_path_raises():
    with pytest.raises(FileNotFoundError):
        cd(["/__no_such_dir__"])


def test_cd_path_is_file_raises(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        cd([str(f)])