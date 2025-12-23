from unittest.mock import Mock, patch
import src.commands.rm as mod_rm


class TestRm:
    def test_rm_file_yes(self):
        target = "/ye.txt"
        m_move = Mock()

        with patch("builtins.input", return_value="y"), \
             patch.object(mod_rm.os.path, "exists", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isfile", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isdir", return_value=False), \
             patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm([target])

        m_move.assert_called_once()
        assert m_move.call_args.args[0] == target

    def test_rm_file_no(self):
        target = "/kanye.txt"
        m_move = Mock()

        with patch("builtins.input", return_value="n"), \
             patch.object(mod_rm.os.path, "exists", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isfile", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isdir", return_value=False), \
             patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm([target])

        m_move.assert_not_called()

    def test_rm_dir_without_r_raises(self):
        target = "/dir"
        m_move = Mock()

        with patch("builtins.input", return_value="y"), \
             patch.object(mod_rm.os.path, "exists", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isfile", return_value=False), \
             patch.object(mod_rm.os.path, "isdir", side_effect=lambda p: p == target), \
             patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm([target])

        m_move.assert_not_called()

    def test_rm_dir_with_r_yes(self):
        target = "/dir"
        m_move = Mock()

        with patch("builtins.input", return_value="y"), \
             patch.object(mod_rm.os.path, "exists", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isfile", return_value=False), \
             patch.object(mod_rm.os.path, "isdir", side_effect=lambda p: p == target), \
             patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm(["-r", target])

        m_move.assert_called_once()
        assert m_move.call_args.args[0] == target

    def test_rm_dir_with_r_no(self):
        target = "/dir"
        m_move = Mock()

        with patch("builtins.input", return_value="n"), \
             patch.object(mod_rm.os.path, "exists", side_effect=lambda p: p == target), \
             patch.object(mod_rm.os.path, "isfile", return_value=False), \
             patch.object(mod_rm.os.path, "isdir", side_effect=lambda p: p == target), \
             patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm(["-r", target])

        m_move.assert_not_called()

    def test_rm_missing_path_raises(self):
        missing = "/nope"
        m_move = Mock()

        with patch.object(mod_rm.os.path, "exists", return_value=False), \
             patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm([missing])

        m_move.assert_not_called()

    def test_rm_protects_root(self):
        m_move = Mock()

        with patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm(["/"])

        m_move.assert_not_called()

    def test_rm_protects_root_r(self):
        m_move = Mock()

        with patch.object(mod_rm.shutil, "move", m_move):
            mod_rm.rm(["-r", "/"])

        m_move.assert_not_called()