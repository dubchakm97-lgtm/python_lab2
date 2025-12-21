import pytest
from unittest.mock import Mock, patch
import os
import src.commands.rm as mod_rm


class TestRm:
    def test_rm_file_yes(self):
        target = "/ye.txt"
        m_path = Mock(spec=os.path)
        m_path.exists.side_effect = lambda p: p == target
        m_path.isfile.side_effect = lambda p: p == target
        m_path.isdir.side_effect = lambda p: False
        m_remove = Mock()
        with patch("builtins.input", Mock(return_value="y")), \
                patch.object(mod_rm.os, "path", m_path), \
                patch.object(mod_rm.os, "remove", m_remove):
            mod_rm.rm([target])
        m_remove.assert_called_once_with(target)

    def test_rm_file_no(self):
        target = "/kanye.txt"
        m_path = Mock(spec=os.path)
        m_path.exists.side_effect = lambda p: p == target
        m_path.isfile.side_effect = lambda p: p == target
        m_path.isdir.side_effect = lambda p: False
        m_remove = Mock()
        with patch("builtins.input", Mock(return_value="n")), \
                patch.object(mod_rm.os, "path", m_path), \
                patch.object(mod_rm.os, "remove", m_remove):
            mod_rm.rm([target])
        m_remove.assert_not_called()

    def test_rm_dir_without_r_raises(self):
        target = "/dir"
        m_path = Mock(spec=os.path)
        m_path.exists.side_effect = lambda p: p == target
        m_path.isfile.side_effect = lambda p: False
        m_path.isdir.side_effect = lambda p: p == target
        with patch.object(mod_rm.os, "path", m_path), patch("builtins.input", Mock(return_value="y")):
            with pytest.raises(IsADirectoryError):
                mod_rm.rm([target])

    def test_rm_dir_with_r_yes(self):
        target = "/dir"
        m_path = Mock(spec=os.path)
        m_path.exists.side_effect = lambda p: p == target
        m_path.isfile.side_effect = lambda p: False
        m_path.isdir.side_effect = lambda p: p == target
        m_rmtree = Mock()
        with patch("builtins.input", Mock(return_value="y")), \
                patch.object(mod_rm.os, "path", m_path), \
                patch.object(mod_rm.shutil, "rmtree", m_rmtree):
            mod_rm.rm(["-r", target])
        m_rmtree.assert_called_once_with(target)

    def test_rm_dir_with_r_no(self):
        target = "/dir"
        m_path = Mock(spec=os.path)
        m_path.exists.side_effect = lambda p: p == target
        m_path.isfile.side_effect = lambda p: False
        m_path.isdir.side_effect = lambda p: p == target
        m_rmtree = Mock()
        with patch("builtins.input", Mock(return_value="n")), \
                patch.object(mod_rm.os, "path", m_path), \
                patch.object(mod_rm.shutil, "rmtree", m_rmtree):
            mod_rm.rm(["-r", target])

        m_rmtree.assert_not_called()

    def test_rm_missing_path_raises(self):
        missing = "/nope"
        m_path = Mock(spec=os.path)
        m_path.exists.side_effect = lambda p: False
        m_path.isfile.side_effect = lambda p: False
        m_path.isdir.side_effect = lambda p: False
        with patch.object(mod_rm.os, "path", m_path):
            with pytest.raises(OSError):
                mod_rm.rm([missing])

    def test_rm_protects_root(self):
        with patch.object(mod_rm.os, "remove") as m_remove, patch.object(mod_rm.shutil, "rmtree") as m_rmtree:
            with pytest.raises(PermissionError):
                mod_rm.rm(["/"])
        m_remove.assert_not_called()
        m_rmtree.assert_not_called()

    def test_rm_protects_root_r(self):
        with patch.object(mod_rm.os, "remove") as m_remove, patch.object(mod_rm.shutil, "rmtree") as m_rmtree:
            with pytest.raises(PermissionError):
                mod_rm.rm(["-r", "/"])
        m_remove.assert_not_called()
        m_rmtree.assert_not_called()
