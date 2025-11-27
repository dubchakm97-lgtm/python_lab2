import pytest
from unittest.mock import Mock, patch
import src.cp as mod_cp

class TestCp:
    def test_cp_file_file(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = True
        src.is_dir.return_value = False

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst
        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
                patch.object(mod_cp.shutil, "copy2") as m_copy2, \
                patch("builtins.print") as m_print:
            mod_cp.cp(["a.txt", "b.txt"])
        m_copy2.assert_called_once_with(src, dst)
        assert any("Скопировано" in str(c.args) for c in m_print.call_args_list)

    def test_cp_file_dir(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = True
        src.is_dir.return_value = False

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst
        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
                patch.object(mod_cp.shutil, "copy2") as m_copy2, \
                patch("builtins.print") as m_print:
            mod_cp.cp(["a.txt", "some_dir"])
        m_copy2.assert_called_once_with(src, dst)
        assert any("Скопировано" in str(c.args) for c in m_print.call_args_list)

    def test_cp_not_source(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = False

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst
        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]):
            with pytest.raises(FileNotFoundError):
                mod_cp.cp(["nope.txt", "b.txt"])

    def test_cp_dir_withaut_r(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = True
        src.is_dir.return_value = True
        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst
        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]):
            with pytest.raises(IsADirectoryError):
                mod_cp.cp(["folder", "dst"])

    def test_cp_dir_with_r(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = True
        src.is_dir.return_value = True

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst
        dst.exists.return_value = False
        dst.is_dir.return_value = False
        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
             patch.object(mod_cp.shutil, "copytree") as m_copy2, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["-r", "folder", "dst"])
        m_copy2.assert_called_once_with(src, dst, dirs_exist_ok=True)
        assert any("Скопировано" in str(c.args) for c in m_print.call_args_list)

    def test_cp_not_enough_args(self):
        with pytest.raises(ValueError):
            mod_cp.cp(["only_one"])