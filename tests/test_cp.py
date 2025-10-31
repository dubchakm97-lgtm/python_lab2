import pytest
from cp import cp

def test_cp_file_to_file(tmp_path):
    src_file = tmp_path / "a.txt"
    dst_file = tmp_path / "b.txt"
    src_file.write_text("hello", encoding="utf-8")

    cp([str(src_file), str(dst_file)])

    assert src_file.exists()
    assert dst_file.exists()
    assert dst_file.read_text(encoding="utf-8") == "hello"

def test_cp_file_into_folder(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("x", encoding="utf-8")
    folder = tmp_path / "dst"
    folder.mkdir()

    cp([str(src), str(folder)])

    copied = folder / "a.txt"
    assert copied.exists()
    assert copied.read_text(encoding="utf-8") == "x"

def test_cp_missing_source_raises():
    with pytest.raises(FileNotFoundError):
        cp(["/__nope__", "/tmp/whatever"])

def test_cp_dir_without_flag_raises(tmp_path):
    d = tmp_path / "stuff"
    d.mkdir()
    (d / "f.txt").write_text("1", encoding="utf-8")

    with pytest.raises(IsADirectoryError):
        cp([str(d), str(tmp_path / "copy")])

def test_cp_dir_with_r_ok(tmp_path):
    d = tmp_path / "stuff"
    d.mkdir()
    (d / "f.txt").write_text("1", encoding="utf-8")
    dst = tmp_path / "copy"

    cp(["-r", str(d), str(dst)])

    assert (dst / "f.txt").exists()
    assert (dst / "f.txt").read_text(encoding="utf-8") == "1"
