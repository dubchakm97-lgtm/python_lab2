import pytest
from rm import rm

def test_rm_file_yes(tmp_path, fake_input):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fake_input(["y"])
    rm([str(f)])
    assert not f.exists()

def test_rm_file_no(tmp_path, fake_input):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fake_input(["n"])
    rm([str(f)])
    assert f.exists()

def test_rm_dir_without_r_raises(tmp_path, fake_input):
    d = tmp_path / "d"
    (d / "x.txt").parent.mkdir()
    (d / "x.txt").write_text("1", encoding="utf-8")
    fake_input(["y"])
    with pytest.raises(IsADirectoryError):
        rm([str(d)])

def test_rm_dir_with_r_yes(tmp_path, fake_input):
    d = tmp_path / "d"
    (d / "x.txt").parent.mkdir()
    (d / "x.txt").write_text("1", encoding="utf-8")
    fake_input(["y"])
    rm(["-r", str(d)])
    assert not d.exists()

def test_rm_dir_with_r_no(tmp_path, fake_input):
    d = tmp_path / "d"
    d.mkdir()
    fake_input(["n"])
    rm(["-r", str(d)])
    assert d.exists()

def test_rm_missing_path_raises():
    with pytest.raises(FileNotFoundError):
        rm(["/ALIVE"])

def test_rm_logs_success_file(tmp_path, fake_input):
    from log import LOG_FILE
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fake_input(["y"])
    rm([str(f)])
    text = (tmp_path / "shell.log").read_text(encoding="utf-8")
    assert "rm " in text and "a.txt" in text
