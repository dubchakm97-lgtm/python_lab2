import builtins
import pytest
from main import main

def test_main_quit(monkeypatch, capsys):
    seq = iter(["quit"])
    monkeypatch.setattr(builtins, "input", lambda _="": next(seq))
    main()
    out = capsys.readouterr().out
    assert isinstance(out, str)

def test_main_ls_then_quit(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    seq = iter(["ls", "quit"])
    monkeypatch.setattr(builtins, "input", lambda _="": next(seq))
    main()
    out = capsys.readouterr().out
    assert "a.txt" in out

def test_main_unknown_command(monkeypatch, capsys):
    seq = iter(["abracadabra", "quit"])
    monkeypatch.setattr(builtins, "input", lambda _="": next(seq))
    main()
    out = capsys.readouterr().out
    assert "Неизвестная команда" in out

def test_main_handles_command_error(monkeypatch, capsys):
    seq = iter(["cat /__no_such__", "quit"])
    monkeypatch.setattr(builtins, "input", lambda _="": next(seq))
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() crashed with exception: {e}")
    out = capsys.readouterr().out
    assert "Ошибка" in out or "существует" in out or "not found" in out