import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import src.commands.command_undo as mod_undo

class TestUndo:
    def _make_log(self, lines: list[str]):
        data = "\n".join(lines) + "\n"
        m_open = mock_open(read_data=data)
        fake_shell_file = Mock()
        fake_shell_file.open = m_open
        return fake_shell_file

    def test_undo_no_commands(self):
        lines = ["[2025-11-27 10:00] ls", "[2025-11-27 10:01] cd /work"]
        fake_shell_file = self._make_log(lines)
        with patch.object(mod_undo, "SHELL_FILE", fake_shell_file), \
             patch.object(mod_undo, "log_message") as m_log, \
             patch("builtins.print") as m_print:
            mod_undo.undo()
        assert any("Нет команд для отката" in " ".join(map(str, c.args))
                   for c in m_print.call_args_list)
        m_log.assert_any_call("No rm/mv/cp commands to undo")

    def test_undo_rm_success(self):
        lines = ["[2025-11-27 10:00] some other command", "[2025-11-27 10:01] rm '/file.txt' from '/original/dir'"]
        fake_shell_file = self._make_log(lines)
        with patch.object(mod_undo, "SHELL_FILE", fake_shell_file), \
             patch.object(mod_undo.shutil, "move") as m_move, \
             patch.object(mod_undo, "log_message") as m_log, \
             patch("builtins.print") as m_print:
            mod_undo.undo()
        name = "/file.txt"
        expected_src = mod_undo.TRASH_DIR / name
        expected_dst = Path("/original/dir")
        m_move.assert_called_once_with(expected_src, expected_dst)
        assert any("восстановлен" in " ".join(map(str, c.args)).lower()
                   for c in m_print.call_args_list)
        assert any("Undo rm" in args[0] for args, _ in m_log.call_args_list)

    def test_undo_mv_success(self):
        lines = ["[2025-11-27 10:10] mv /work/a.txt /work/b.txt"]
        fake_shell_file = self._make_log(lines)
        src_path = Mock()
        src_path.expanduser.return_value = src_path

        dst_path = Mock()
        dst_path.expanduser.return_value = dst_path
        dst_path.is_dir.return_value = False
        with patch.object(mod_undo, "SHELL_FILE", fake_shell_file), \
             patch.object(mod_undo, "Path", side_effect=[src_path, dst_path]), \
             patch.object(mod_undo.shutil, "move") as m_move, \
             patch.object(mod_undo, "log_message") as m_log, \
             patch("builtins.print") as m_print:
            mod_undo.undo()
        m_move.assert_called_once_with(dst_path, src_path)
        assert any("объект возвращён" in " ".join(map(str, c.args)).lower()
                   for c in m_print.call_args_list)
        assert any("Undo mv" in args[0] for args, _ in m_log.call_args_list)

    def test_undo_cp_file_success(self):
        lines = ["[2025-11-27 10:20] cp /work/a.txt /work/b.txt"]
        fake_shell_file = self._make_log(lines)
        src_path = Mock()
        src_path.expanduser.return_value = src_path

        dst_path = Mock()
        dst_path.expanduser.return_value = dst_path
        dst_path.is_dir.return_value = False
        dst_path.exists.return_value = True
        dst_path.is_dir.return_value = False
        with patch.object(mod_undo, "SHELL_FILE", fake_shell_file), \
             patch.object(mod_undo, "Path", side_effect=[src_path, dst_path]), \
             patch.object(mod_undo.shutil, "rmtree") as m_rmtree, \
             patch.object(mod_undo, "log_message") as m_log, \
             patch("builtins.print") as m_print:
            dst_path.unlink = Mock()
            mod_undo.undo()
        dst_path.unlink.assert_called_once()
        m_rmtree.assert_not_called()
        assert any("копия" in " ".join(map(str, c.args)).lower() for c in m_print.call_args_list)
        assert any("Undo cp remove" in args[0] for args, _ in m_log.call_args_list)