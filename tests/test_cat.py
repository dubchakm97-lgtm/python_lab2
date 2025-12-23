from unittest.mock import patch, mock_open
import src.commands.cat as mod_cat


class TestCat:
    def test_cat_prints_file(self, capsys):
        destination = "/file.txt"

        with patch.object(mod_cat.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cat.os.path, "exists", return_value=True), \
             patch.object(mod_cat.os.path, "isfile", return_value=True), \
             patch("builtins.open", mock_open(read_data="HELLO")):
            mod_cat.cat([destination])

        out = capsys.readouterr().out
        assert "HELLO" in out

    def test_cat_do_not_exist_(self, capsys):
        destination = "/missing.txt"

        with patch.object(mod_cat.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cat.os.path, "exists", return_value=False):
            mod_cat.cat([destination])

        out = capsys.readouterr().out
        assert "Такого файла не существует" in out

    def test_cat_no_file(self, capsys):
        mod_cat.cat([])
        out = capsys.readouterr().out
        assert "Не указан файл" in out

    def test_cat_directory_path(self, capsys):
        dir_path = "/some_ye"
        with patch.object(mod_cat.os.path, "expanduser", side_effect=lambda p: p), \
             patch.object(mod_cat.os.path, "exists", return_value=True), \
             patch.object(mod_cat.os.path, "isfile", return_value=False):
            mod_cat.cat([dir_path])
        out = capsys.readouterr().out
        assert "Это не файл" in out