import pytest
from unittest.mock import Mock, patch
import src.cd as mod_cd
import os

class TestCd:

    def test_cd_into_existing_dir(self, capsys):
        destination = '/correct_dir'
        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.side_effect = lambda p: p == destination
        m_path.isdir.side_effect = lambda p: p == destination
        state = Mock();
        state.cwd = "/start"
        def _chdir(p):
            if not (m_path.exists(p) and m_path.isdir(p)):
                raise FileNotFoundError
            state.cwd = p
        def _getcwd(): return state.cwd
        with patch.object(mod_cd.os, "path", m_path), \
                patch.object(mod_cd.os, "chdir", _chdir), \
                patch.object(mod_cd.os, "getcwd", _getcwd):
            mod_cd.cd([destination])
            assert mod_cd.os.getcwd() == destination
            assert "Текущая директория:" in capsys.readouterr().out

    def test_is_not_dir(self):
        destination = "/file.txt"
        m_chdir = Mock()
        with patch.object(mod_cd.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cd.os.path, "exists", side_effect=lambda p: p == destination), \
             patch.object(mod_cd.os.path, "isdir", return_value=False), \
             patch.object(mod_cd.os, "chdir", m_chdir):
            with pytest.raises(NotADirectoryError) as er:
                mod_cd.cd([destination])
        m_chdir.assert_not_called()
        assert "Это не директория" in str(er.value)


    def test_is_non_exist_dir(self):
        destination = "/yeezy"
        m_path = Mock(spec=os.path)
        m_chdir = Mock()
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.side_effect = lambda p: False
        m_path.isdir.side_effect = lambda p: False
        with patch.object(mod_cd.os, 'chdir', m_chdir), patch.object(mod_cd.os, 'path', m_path):
            with pytest.raises(FileNotFoundError) as er:
                mod_cd.cd([destination])
            assert 'папки не существует' in str(er.value)


    def test_cd_dir_move_without_args(self, capsys):
        destination = "/home"
        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: destination if p == "~" else p
        m_path.exists.return_value = True
        m_path.isdir.return_value = True
        state = Mock();
        state.cwd = "/start"
        def _chdir(p): state.cwd = p
        def _getcwd(): return state.cwd
        with patch.object(mod_cd.os, "path", m_path), \
                patch.object(mod_cd.os, "chdir", _chdir), \
                patch.object(mod_cd.os, "getcwd", _getcwd):
            mod_cd.cd([])
            assert mod_cd.os.getcwd() == destination
            out = capsys.readouterr().out
            assert "Текущая директория:" in out
            assert destination in out