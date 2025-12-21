import pytest
from unittest.mock import Mock, MagicMock, patch
import src.commands.grep as mod_grep


class TestGrep:
    def test_grep_simple_match(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = True
        path.is_dir.return_value = False

        fobj = MagicMock()
        fobj.readlines.return_value = ["foo bar\n", "something\n"]
        cm = MagicMock()
        cm.__enter__.return_value = fobj
        path.open.return_value = cm

        with patch.object(mod_grep, "Path", return_value=path), \
             patch.object(mod_grep, "log_message") as m_log, \
             patch("builtins.print") as m_print:

            mod_grep.grep(["foo", "file.txt"])

        printed = [" ".join(map(str, c.args)) for c in m_print.call_args_list]
        assert any("foo bar" in line for line in printed)
        assert any("grep match 'foo'" in args[0] for args, _ in m_log.call_args_list)

    def test_grep_file_not_exists(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = False

        with patch.object(mod_grep, "Path", return_value=path), \
             patch.object(mod_grep, "log_message"):
            with pytest.raises(FileNotFoundError):
                mod_grep.grep(["foo", "nope.txt"])

    def test_grep_i_case_insensitive(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = True
        path.is_dir.return_value = False

        fobj = MagicMock()
        fobj.readlines.return_value = ["Foo BAR\n", "xxx\n"]
        cm = MagicMock()
        cm.__enter__.return_value = fobj
        path.open.return_value = cm

        with patch.object(mod_grep, "Path", return_value=path), \
             patch.object(mod_grep, "log_message") as m_log, \
             patch("builtins.print") as m_print:

            mod_grep.grep(["foo", "file.txt", "-i"])

        printed = [" ".join(map(str, c.args)) for c in m_print.call_args_list]
        assert any("Foo BAR" in line for line in printed)
        assert any("grep -i match 'foo'" in args[0] for args, _ in m_log.call_args_list)

    def test_grep_r_directory(self):
        root = Mock()
        root.expanduser.return_value = root
        root.exists.return_value = True
        root.is_file.return_value = False

        file1 = Mock()
        file1.is_file.return_value = True
        file2 = Mock()
        file2.is_file.return_value = True

        root.rglob.return_value = [file1, file2]

        f1_obj = MagicMock()
        f1_obj.readlines.return_value = ["foo here\n"]
        f1_cm = MagicMock()
        f1_cm.__enter__.return_value = f1_obj
        file1.open.return_value = f1_cm

        f2_obj = MagicMock()
        f2_obj.readlines.return_value = ["nothing\n"]
        f2_cm = MagicMock()
        f2_cm.__enter__.return_value = f2_obj
        file2.open.return_value = f2_cm

        with patch.object(mod_grep, "Path", return_value=root), \
             patch.object(mod_grep, "log_message") as m_log, \
             patch("builtins.print") as m_print:
            mod_grep.grep(["foo", "folder", "-r"])

        printed = [" ".join(map(str, c.args)) for c in m_print.call_args_list]
        assert sum("foo here" in line for line in printed) == 1
        assert any("grep match -r 'foo'" in args[0] for args, _ in m_log.call_args_list)