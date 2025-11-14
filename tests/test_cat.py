import pytest
from unittest.mock import Mock, patch, mock_open
import src.cat as mod_cat
import os

class TestCat:
    def test_cat_prints_file(self, capsys):
        destination = "/file.txt"

        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.side_effect = lambda p: p == destination
        m_path.isfile.side_effect = lambda p: p == destination

        with patch.object(mod_cat.os, "path", m_path), \
             patch("builtins.open", mock_open(read_data="HELLO")):
            mod_cat.cat([destination])

        out = capsys.readouterr().out
        assert "HELLO" in out

    def test_cat_do_not_exist_(self):
        destination = "/missing.txt"

        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.return_value = False
        m_path.isfile.return_value = False

        with patch.object(mod_cat.os, "path", m_path):
            with pytest.raises(FileNotFoundError):
                mod_cat.cat([destination])

    def test_cat_path_is_directory(self):
        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.return_value = True
        m_path.isfile.return_value = False

        with patch.object(mod_cat.os, "path", m_path):
            with pytest.raises(ValueError) as er:
                mod_cat.cat([])
            assert "Не указан файл" in str(er.value)

    def test_cat_directory_path(self):
        dir_path = "/some_ye"

        m_path = Mock(spec=os.path)
        m_path.expanduser.side_effect = lambda p: p
        m_path.exists.return_value = True
        m_path.isfile.return_value = False

        with patch.object(mod_cat.os, "path", m_path):
            with pytest.raises(IsADirectoryError) as er:
                mod_cat.cat([dir_path])
            assert "не файл" in str(er.value)