import os
import pytest
import log
from cat import cat

def test_cat_reading_file(tmp_path, capsys):
    log.LOG_FILE = tmp_path / "shell.log"
    os.chdir(tmp_path)
    f = tmp_path / "a.txt"
    f.write_text('THE', encoding="utf-8")
    cat([str(f)])
    out = capsys.readouterr().out.strip()
    assert 'THE' in out

def test_cat_file_not_found():
    with pytest.raises(FileNotFoundError):
        cat(["/BEST.txt"])

def test_cat_path_is_directory(tmp_path):
    d = tmp_path / "dir"
    d.mkdir()
    with pytest.raises(IsADirectoryError):
        cat([str(d)])