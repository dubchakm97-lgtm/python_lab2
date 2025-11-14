import pytest
from unittest.mock import Mock, patch
import src.ls as mod_ls
import os
import datetime

class TestLs:
    def test_ls_nonexistent_path_raises(self):
        m_path = Mock(spec=os.path)
        m_path.exists.return_value = False
        with patch.object(mod_ls.os, "path", m_path):
            with pytest.raises(FileNotFoundError):
                mod_ls.ls(["/missing"])

    def test_ls_prints_file_path(self):
        target = "/FUTURE/a.txt"
        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.return_value = True
        m_path.isfile.return_value = True
        with patch.object(mod_ls.os, "path", m_path), \
             patch("builtins.print") as m_print:
            mod_ls.ls([target])
        m_print.assert_called_once_with(target)

    def test_ls_lists_directory(self):
        p = "/dir"
        m_path = Mock(spec=os.path)
        m_path.exists.return_value = True
        m_path.isfile.return_value = False
        with patch.object(mod_ls.os, "path", m_path), \
             patch.object(mod_ls.os, "listdir", return_value=["b.txt", "a.txt"]), \
             patch("builtins.print") as m_print:
            mod_ls.ls([p])
        calls = [c.args[0] for c in m_print.call_args_list]
        assert "a.txt" in calls and "b.txt" in calls

    def test_ls_long_format_for_dir(self):
        p = "/dir"
        m_path = Mock(spec=os.path)
        m_path.exists.return_value = True
        m_path.isfile.return_value = False

        def fake_stat(_):
            o = Mock()
            o.st_size = 123
            o.st_mtime = 1700000000
            return o

        with patch.object(mod_ls.os, "path", m_path), \
             patch.object(mod_ls.os, "listdir", return_value=["x.txt"]), \
             patch.object(mod_ls.os, "stat", side_effect=fake_stat), \
             patch.object(mod_ls.datetime, "datetime") as m_dt, \
             patch("builtins.print") as m_print:
            m_dt.fromtimestamp.return_value = datetime.datetime(2023, 1, 1, 12, 0)
            mod_ls.ls(["-l", p])
        out = " ".join(c.args[0] for c in m_print.call_args_list)
        assert "x.txt" in out and "bytes" in out

    def test_ls_default_cwd_with_l(self):
        m_path = Mock(spec=os.path)
        m_path.exists.return_value = True
        m_path.isfile.return_value = False
        with patch.object(mod_ls.os, "path", m_path), \
             patch.object(mod_ls.os, "listdir", return_value=["here.txt"]), \
             patch.object(mod_ls.os, "stat", return_value=Mock(st_size=1, st_mtime=1700000000)), \
             patch.object(mod_ls.datetime, "datetime") as m_dt, \
             patch("builtins.print") as m_print:
            m_dt.fromtimestamp.return_value = datetime.datetime(2023, 1, 1, 12, 0)
            mod_ls.ls(["-l"])
        out = " ".join(c.args[0] for c in m_print.call_args_list)
        assert "here.txt" in out and "bytes" in out