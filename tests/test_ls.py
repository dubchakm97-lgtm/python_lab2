from unittest.mock import Mock, patch
import src.commands.ls as mod_ls
import datetime


class TestLs:
    def test_ls_nonex_path(self):
        with patch.object(mod_ls.os.path, "exists", return_value=False), \
                patch("builtins.print") as m_print:
            mod_ls.ls(["/missing"])

        out = " ".join(str(c.args[0]) for c in m_print.call_args_list)
        assert "cannot access" in out

    def test_ls_print_path(self):
        target = "/FUTURE/a.txt"
        with patch.object(mod_ls.os.path, "expanduser", side_effect=lambda p: p), \
                patch.object(mod_ls.os.path, "exists", return_value=True), \
                patch.object(mod_ls.os.path, "isfile", return_value=True), \
                patch("builtins.print") as m_print:
            mod_ls.ls([target])

        calls = [c.args[0] for c in m_print.call_args_list if c.args]
        assert target in calls

    def test_ls_print_directory(self):
        p = "/dir"
        with patch.object(mod_ls.os.path, "expanduser", side_effect=lambda x: x), \
                patch.object(mod_ls.os.path, "exists", return_value=True), \
                patch.object(mod_ls.os.path, "isfile", return_value=False), \
                patch.object(mod_ls.os, "listdir", return_value=["b.txt", "a.txt"]), \
                patch("builtins.print") as m_print:
            mod_ls.ls([p])

        calls = [c.args[0] for c in m_print.call_args_list if c.args]
        assert "a.txt" in calls and "b.txt" in calls

    def test_lsl_dir(self):
        p = "/dir"

        def fake_stat(_):
            o = Mock()
            o.st_size = 123
            o.st_mtime = 1700000000
            return o

        with patch.object(mod_ls.os.path, "expanduser", side_effect=lambda x: x), \
                patch.object(mod_ls.os.path, "exists", return_value=True), \
                patch.object(mod_ls.os.path, "isfile", return_value=False), \
                patch.object(mod_ls.os.path, "join", side_effect=lambda a, b: f"{a}/{b}"), \
                patch.object(mod_ls.os, "listdir", return_value=["x.txt"]), \
                patch.object(mod_ls.os, "stat", side_effect=fake_stat), \
                patch.object(mod_ls.datetime, "datetime") as m_dt, \
                patch("builtins.print") as m_print:
            m_dt.fromtimestamp.return_value = datetime.datetime(2023, 1, 1, 12, 0)
            mod_ls.ls(["-l", p])

        out = " ".join(str(c.args[0]) for c in m_print.call_args_list if c.args)
        assert "x.txt" in out and "bytes" in out

    def test_lsl(self):
        with patch.object(mod_ls.os.path, "exists", return_value=True), \
                patch.object(mod_ls.os.path, "isfile", return_value=False), \
                patch.object(mod_ls.os, "listdir", return_value=["here.txt"]), \
                patch.object(mod_ls.os.path, "join", side_effect=lambda a, b: f"{a}/{b}"), \
                patch.object(mod_ls.os, "stat", return_value=Mock(st_size=1, st_mtime=1700000000)), \
                patch.object(mod_ls.datetime, "datetime") as m_dt, \
                patch("builtins.print") as m_print:
            m_dt.fromtimestamp.return_value = datetime.datetime(2025, 1, 1, 12, 0)
            mod_ls.ls(["-l"])

        out = " ".join(str(c.args[0]) for c in m_print.call_args_list if c.args)
        assert "here.txt" in out and "bytes" in out
