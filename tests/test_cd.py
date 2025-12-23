from unittest.mock import patch
import src.commands.cd as mod_cd


class TestCd:
    def test_cd_into_existing_dir(self, capsys):
        destination = "/correct_dir"

        with patch.object(mod_cd.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cd.os.path, "exists", side_effect=lambda p: p == destination), \
             patch.object(mod_cd.os.path, "isdir", side_effect=lambda p: p == destination), \
             patch.object(mod_cd.os, "chdir") as m_chdir, \
             patch.object(mod_cd.os, "getcwd", return_value=destination):
            mod_cd.cd([destination])

        m_chdir.assert_called()
        out = capsys.readouterr().out
        assert "Текущая директория:" in out

    def test_is_not_dir(self):
        destination = "/file.txt"

        with patch.object(mod_cd.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cd.os.path, "exists", side_effect=lambda p: p == destination), \
             patch.object(mod_cd.os.path, "isdir", return_value=False), \
             patch.object(mod_cd.os, "chdir") as m_chdir:
            mod_cd.cd([destination])

        m_chdir.assert_not_called()

    def test_is_non_exist_dir(self):
        destination = "/yeezy"

        with patch.object(mod_cd.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cd.os.path, "exists", return_value=False), \
             patch.object(mod_cd.os.path, "isdir", return_value=False), \
             patch.object(mod_cd.os, "chdir") as m_chdir:
            mod_cd.cd([destination])

        m_chdir.assert_not_called()

    def test_cd_dir_move_without_args(self, capsys):
        destination = "/home"

        with patch.object(mod_cd.os.path, "expanduser", side_effect=lambda p: destination if p == "~" else p), \
             patch.object(mod_cd.os.path, "exists", return_value=True), \
             patch.object(mod_cd.os.path, "isdir", return_value=True), \
             patch.object(mod_cd.os, "chdir") as m_chdir, \
             patch.object(mod_cd.os, "getcwd", return_value=destination):
            mod_cd.cd([])

        m_chdir.assert_called()
        out = capsys.readouterr().out
        assert "Текущая директория:" in out
        assert destination in out