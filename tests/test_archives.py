import pytest
from unittest.mock import Mock, patch, MagicMock
import zipfile
import tarfile
import src.commands.archives as mod_arc

class TestFolder:
    def test_zip_folder_success(self):
        src = Mock()
        src.expanduser.return_value = src
        src.exists.return_value = True
        src.is_file.return_value = False

        child = Mock()
        child.is_file.return_value = True
        child.relative_to.return_value = "inner.txt"
        src.rglob.return_value = [child]

        archive = Mock()
        archive.expanduser.return_value = archive
        parent = Mock()
        archive.parent = parent
        parent.exists.return_value = True
        archive.suffix = ".zip"

        zf_obj = Mock()
        zf_cm = MagicMock()
        zf_cm.__enter__.return_value = zf_obj
        zf_cm.__exit__.return_value = None

        with patch.object(mod_arc, "Path", side_effect=[src, archive]), \
             patch.object(mod_arc.zipfile, "ZipFile", return_value=zf_cm), \
             patch("builtins.print") as m_print:
            mod_arc.zip_folder(["folder", "archive.zip"])
        zf_obj.write.assert_called_once_with(child, arcname="inner.txt")
        assert any("Архив" in " ".join(map(str, c.args))
                   for c in m_print.call_args_list)

    def test_zip_folder_not_enough_args(self):
        with pytest.raises(ValueError):
            mod_arc.zip_folder(["only_folder"])

    def test_zip_folder_bad_name_too_short(self):
        with patch.object(mod_arc, "Path") as m_path:
            m_path.return_value = Mock()
            with pytest.raises(ValueError):
                mod_arc.zip_folder(["folder", "a.zip"])

    def test_unzip_success(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = True
        path.is_file.return_value = True
        path.suffix = ".zip"
        zf_obj = Mock()
        zf_cm = MagicMock()
        zf_cm.__enter__.return_value = zf_obj
        zf_cm.__exit__.return_value = None
        with patch.object(mod_arc, "Path", return_value=path), \
                patch.object(mod_arc.zipfile, "ZipFile", return_value=zf_cm), \
                patch("builtins.print") as m_print:
            mod_arc.unzip_file(["archive.zip"])
        zf_obj.extractall.assert_called_once()
        assert any("распакован" in " ".join(map(str, c.args)).lower()
                   for c in m_print.call_args_list)

    def test_unzip_wrong_args_count(self):
        with pytest.raises(ValueError):
            mod_arc.unzip_file([])
        with pytest.raises(ValueError):
            mod_arc.unzip_file(["a.zip", "extra"])

    def test_unzip_archive_not_exists(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = False
        with patch.object(mod_arc, "Path", return_value=path):
            with pytest.raises(FileNotFoundError):
                mod_arc.unzip_file(["nope.zip"])

    def test_tar_folder_success(self):
        src = Mock()
        src.expanduser.return_value = src
        src.exists.return_value = True
        src.is_file.return_value = False
        child = Mock()
        child.relative_to.return_value = "inner.txt"
        src.rglob.return_value = [child]
        archive = Mock()
        archive.expanduser.return_value = archive
        parent = Mock()
        archive.parent = parent
        parent.exists.return_value = True
        tf_obj = Mock()
        tf_cm = MagicMock()
        tf_cm.__enter__.return_value = tf_obj
        tf_cm.__exit__.return_value = None

        with patch.object(mod_arc, "Path", side_effect=[src, archive]), \
                patch.object(mod_arc.tarfile, "open", return_value=tf_cm), \
                patch("builtins.print") as m_print:
            mod_arc.tar_folder(["folder", "archive.tar.gz"])
        tf_obj.add.assert_called_once_with(child, arcname="inner.txt")
        assert any("Архив" in " ".join(map(str, c.args)) for c in m_print.call_args_list)

    def test_tar_folder_not_enough_args(self):
        with pytest.raises(ValueError):
            mod_arc.tar_folder(["only_folder"])

    def test_tar_folder_bad_name_or_extension(self):
        with pytest.raises(ValueError):
            mod_arc.tar_folder(["folder", "a.tar"])
        with pytest.raises(ValueError):
            mod_arc.tar_folder(["folder", "archive.tar"])

    def test_untar_success(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = True
        path.is_file.return_value = True
        tf_obj = Mock()
        tf_cm = MagicMock()
        tf_cm.__enter__.return_value = tf_obj
        tf_cm.__exit__.return_value = None
        with patch.object(mod_arc, "Path", return_value=path), \
                patch.object(mod_arc.tarfile, "open", return_value=tf_cm), \
                patch("builtins.print") as m_print:
            mod_arc.untar_file(["archive.tar.gz"])
        tf_obj.extractall.assert_called_once()
        assert any("распакован" in " ".join(map(str, c.args)).lower()
                   for c in m_print.call_args_list)

    def test_untar_wrong_args_count(self):
        with pytest.raises(ValueError):
            mod_arc.untar_file([])
        with pytest.raises(ValueError):
            mod_arc.untar_file(["a.tar.gz", "extra"])

    def test_untar_archive_not_exists(self):
        path = Mock()
        path.expanduser.return_value = path
        path.exists.return_value = False
        with patch.object(mod_arc, "Path", return_value=path):
            with pytest.raises(FileNotFoundError):
                mod_arc.untar_file(["nope.tar.gz"])