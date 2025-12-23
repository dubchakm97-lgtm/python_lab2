from unittest.mock import Mock, patch
import src.commands.cp as mod_cp


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
        dst.is_dir.return_value = False

        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
             patch.object(mod_cp.shutil, "copy2") as m_copy2, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["a.txt", "b.txt"])

        m_copy2.assert_called_once_with(src, dst)
        assert any("скоп" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)

    def test_cp_file_dir(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = True
        src.is_dir.return_value = False

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst
        dst.is_dir.return_value = True

        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
             patch.object(mod_cp.shutil, "copy2") as m_copy2, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["a.txt", "some_dir"])

        assert m_copy2.call_count == 1
        assert any("скоп" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)

    def test_cp_not_source(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = False

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst

        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
             patch.object(mod_cp.shutil, "copy2") as m_copy2, \
             patch.object(mod_cp.shutil, "copytree") as m_copytree, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["nope.txt", "b.txt"])

        m_copy2.assert_not_called()
        m_copytree.assert_not_called()
        assert any("ошибка" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)

    def test_cp_dir_without_r(self):
        src = Mock()
        src.expanduser.return_value = src
        src.resolve.return_value = src
        src.exists.return_value = True
        src.is_dir.return_value = True

        dst = Mock()
        dst.expanduser.return_value = dst
        dst.resolve.return_value = dst

        with patch.object(mod_cp.pathlib, "Path", side_effect=[src, dst]), \
             patch.object(mod_cp.shutil, "copy2") as m_copy2, \
             patch.object(mod_cp.shutil, "copytree") as m_copytree, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["folder", "dst"])

        m_copy2.assert_not_called()
        m_copytree.assert_not_called()
        assert any("ошибка" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)

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
             patch.object(mod_cp.shutil, "copytree") as m_copytree, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["-r", "folder", "dst"])

        m_copytree.assert_called_once_with(src, dst, dirs_exist_ok=True)
        assert any("скоп" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)

    def test_cp_not_enough_args(self):
        with patch.object(mod_cp.shutil, "copy2") as m_copy2, \
             patch.object(mod_cp.shutil, "copytree") as m_copytree, \
             patch("builtins.print") as m_print:
            mod_cp.cp(["only_one"])

        m_copy2.assert_not_called()
        m_copytree.assert_not_called()
        assert any("ошибка" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)