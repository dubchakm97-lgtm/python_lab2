import pytest
import log
from mv import mv


def test_mv_rename_file_same_dir(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text("x", encoding="utf-8")
    b = tmp_path / "b.txt"
    mv([str(a), str(b)])
    assert not a.exists()
    assert b.exists()
    assert b.read_text(encoding="utf-8") == "x"


def test_mv_move_file_into_dir(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text("x", encoding="utf-8")
    dst = tmp_path / "dst"
    dst.mkdir()
    mv([str(a), str(dst)])
    assert not a.exists()
    assert (dst / "a.txt").exists()


def test_mv_source_not_found():
    with pytest.raises(FileNotFoundError):
        mv(["/RAPPER", "x"])


def test_mv_move_directory_into_dir(tmp_path):
    srcd = tmp_path / "srcd"
    srcd.mkdir()
    (srcd / "inside.txt").write_text("1", encoding="utf-8")
    dst = tmp_path / "dst"
    dst.mkdir()
    mv([str(srcd), str(dst)])
    assert not srcd.exists()
    assert (dst / "srcd" / "inside.txt").exists()


def test_mv_logs_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        mv([str(tmp_path / "missing.txt"), str(tmp_path / "b.txt")])
    log_text = (tmp_path / "shell.log").read_text(encoding="utf-8")
    assert "ERROR: mv" in log_text