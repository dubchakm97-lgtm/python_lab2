from unittest.mock import Mock, patch
import src.commands.mv as mod_mv


class TestMv:
    def setup_method(self):
        self.src = "/work/a.txt"
        self.dst = "/work/b.txt"
        self.dst_dir = "/work/dir"

    def test_rename_file_same_dir(self):
        m_move = Mock()
        with patch.object(mod_mv.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_mv.os.path, "exists", return_value=True), \
             patch.object(mod_mv.shutil, "move", m_move):
            mod_mv.mv([self.src, self.dst])
        m_move.assert_called_once_with(self.src, self.dst)

    def test_move_file_into_dir(self):
        m_move = Mock()
        with patch.object(mod_mv.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_mv.os.path, "exists", return_value=True), \
             patch.object(mod_mv.shutil, "move", m_move):
            mod_mv.mv([self.src, self.dst_dir])
        m_move.assert_called_once_with(self.src, self.dst_dir)

    def test_source_not_found_raises(self):
        with patch.object(mod_mv.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_mv.os.path, "exists", return_value=False):
            mod_mv.mv([self.src, self.dst])

    def test_missing_args_raises(self):
        mod_mv.mv([])
        mod_mv.mv([self.src])