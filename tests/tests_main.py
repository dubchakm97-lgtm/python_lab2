import src.main as mod_main
from unittest.mock import Mock, patch

def test_main_ls_then_quit_calls_ls(monkeypatch):
    feeder = iter(["ls", "quit"])
    monkeypatch.setattr("builtins.input", lambda _='': next(feeder))
    m_ls = Mock()
    with patch.object(mod_main, "ls", m_ls):
        mod_main.main()
    m_ls.assert_called_once_with([])

def test_error_com(monkeypatch):
    feeder = iter(["kanye", "quit"])
    monkeypatch.setattr("builtins.input", lambda _='': next(feeder))
    with patch("builtins.print") as m_print:
        mod_main.main()
    assert any("Неизвестная команда" in str(c.args) for c in m_print.call_args_list)

def test_main_unknown_command_(monkeypatch):
    feeder = iter(["ls", "quit"])
    monkeypatch.setattr("builtins.input", lambda _='': next(feeder))
    m_ls = Mock(side_effect=IsADirectoryError)
    with patch.object(mod_main, "ls", m_ls), patch("builtins.print") as m_print:
        mod_main.main()
    assert any("Ошибка" in str(c.args) for c in m_print.call_args_list)