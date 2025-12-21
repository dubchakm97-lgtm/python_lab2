import zipfile
import tarfile
import logging
from pathlib import Path
from src.log import log_message


def zip_folder(args: list[str]) -> None:
    """
    Создает zip-архив указываемой папки
    :param args: список из двух элементов: название папки, название создаваемого архива
    :return: None
    """
    try:
        if len(args) != 2:
            log_message("zip: not enough arguments", logging.WARNING)
            raise ValueError('Нужно указать папку и имя архива: zip "<folder>" "<archive.zip>"')

        path = Path(args[0]).expanduser()
        name = args[1]

        if len(name) < 5:
            log_message("zip: inappropriate name for zip file", logging.WARNING)
            raise ValueError('Укажите верное имя для архива папки')

        archive_path = Path(name).expanduser()
        parent = archive_path.parent

        if not parent.exists():
            log_message("zip: destination folder does not exist", logging.WARNING)
            raise FileNotFoundError('Папки сохранения архива не существует')

        if archive_path.suffix.lower() != '.zip':
            log_message("zip: inappropriate extension (not .zip)", logging.WARNING)
            raise ValueError("Введите имя архива в кавычках с расширением .zip")

        if not path.exists() or path.is_file():
            log_message("zip: path is not existing directory", logging.WARNING)
            raise FileNotFoundError('Такой папки не существует')

        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for child in path.rglob('*'):
                if child.is_file():
                    zf.write(child, arcname=child.relative_to(path))

        print(f"Архив {path} создан в директории {parent}")
        log_message(f"zip {path} -> {archive_path}", logging.INFO)

    except PermissionError as p:
        log_message(f"zip: permission error ({p})", logging.ERROR)
        print('Недостаточно прав для создания zip-архива для файла')
    except Exception as e:
        print("Ошибка при архивировании папки: ", e)
        log_message(f"zip: exception ({e})", logging.ERROR)


def unzip_file(args: list[str]) -> None:
    """
    Распаковывает zip-архив
    :param args: название zip-архива в текущей директории
    :return: None
    """
    try:
        if len(args) != 1:
            log_message("unzip: inappropriate number of arguments", logging.WARNING)
            raise ValueError('В качестве аргумента к команде unzip укажите только файл для разархивирования')

        path = Path(args[0]).expanduser()

        if not path.exists():
            log_message("unzip: zip archive does not exist", logging.WARNING)
            raise FileNotFoundError('В текущем каталоге такого архива не существует')

        if not path.is_file() or path.suffix.lower() != '.zip':
            log_message("unzip: it is not a zip file", logging.WARNING)
            raise ValueError('Выбранный файл для разархивирования не является zip архивом')

        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall()

        print(f"Архив {path} распакован в текущую директорию")
        log_message(f"unzip {path}", logging.INFO)

    except zipfile.BadZipFile as e:
        log_message(f"unzip: bad zip ({e})", logging.ERROR)
        print("Файл не является корректным zip архивом")
    except PermissionError as e:
        log_message(f"unzip: no permission ({e})", logging.ERROR)
        print('Нет прав для разархивирования архива')
    except Exception as e:
        print("Ошибка при разархивировании: ", e)
        log_message(f"unzip: exception ({e})", logging.ERROR)


def tar_folder(args: list[str]) -> None:
    """
    Создает tar.gz-архив указываемой папки
    :param args: список из двух элементов: название папки, название создаваемого архива
    :return: None
    """
    try:
        if len(args) != 2:
            log_message("tar: not enough arguments", logging.WARNING)
            raise ValueError('Нужно указать папку и имя архива: tar "<folder>" "<archive.tar.gz>"')

        path = Path(args[0]).expanduser()
        name = args[1]

        if len(name) < 8:
            log_message("tar: inappropriate name for tar.gz file", logging.WARNING)
            raise ValueError('Укажите верное имя для архива папки')

        if not name.lower().endswith(".tar.gz"):
            log_message("tar: inappropriate extension (not .tar.gz)", logging.WARNING)
            raise ValueError("Введите имя архива в кавычках с расширением .tar.gz")

        archive_path = Path(name).expanduser()
        parent = archive_path.parent

        if not parent.exists():
            log_message("tar: destination folder does not exist", logging.WARNING)
            raise FileNotFoundError('Папки сохранения архива не существует')

        if not path.exists() or path.is_file():
            log_message("tar: path is not existing directory", logging.WARNING)
            raise FileNotFoundError('Такой папки не существует')

        with tarfile.open(archive_path, "w:gz") as tf:
            for child in path.rglob("*"):
                tf.add(child, arcname=child.relative_to(path))

        print(f"Архив {path} создан в директории {parent}")
        log_message(f"tar {path} -> {archive_path}", logging.INFO)

    except PermissionError as p:
        log_message(f"tar: permission error ({p})", logging.ERROR)
        print('Недостаточно прав для создания tar.gz-архива для файла')
    except Exception as e:
        print("Ошибка при архивировании папки: ", e)
        log_message(f"tar: exception ({e})", logging.ERROR)


def untar_file(args: list[str]) -> None:
    """
    Распаковывает tar.gz-архив
    :param args: название tar.gz-архива в текущей директории
    :return: None
    """
    try:
        if len(args) != 1:
            log_message("untar: inappropriate number of arguments", logging.WARNING)
            raise ValueError('В качестве аргумента к команде untar укажите только файл для разархивирования')

        path = Path(args[0]).expanduser()

        if not path.exists():
            log_message("untar: tar archive does not exist", logging.WARNING)
            raise FileNotFoundError('В текущем каталоге такого архива не существует')

        if not path.is_file() or not args[0].lower().endswith('.tar.gz'):
            log_message("untar: it is not a tar.gz file", logging.WARNING)
            raise ValueError('Выбранный файл для разархивирования не является tar архивом')

        with tarfile.open(path, "r:gz") as tf:
            tf.extractall()

        print(f"Архив {path} распакован в текущую директорию")
        log_message(f"untar {path}", logging.INFO)

    except tarfile.ReadError as e:
        print("Файл не является корректным tar.gz архивом")
        log_message(f"untar: bad tar.gz ({e})", logging.ERROR)
    except PermissionError as e:
        print("Нет прав для разархивирования архива")
        log_message(f"untar: no permission ({e})", logging.ERROR)
    except Exception as e:
        print("Ошибка при разархивировании: ", e)
        log_message(f"untar: exception ({e})", logging.ERROR)