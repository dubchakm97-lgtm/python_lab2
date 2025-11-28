import zipfile
import tarfile
from pathlib import Path
from log import log_message


def zip_folder(args: list[str]) -> None:
    """
    Создает zip-архив указываемой папки
    :param args: список из двух элементов: название папки, название создаваемого архива
    :return: None
    """
    if len(args) != 2:
        log_message('ERROR: not enough arguments')
        raise ValueError('Нужно указать папку и имя архива: zip "<folder>" "<archive.zip>"')
    path = Path(args[0]).expanduser()
    name = args[1]
    if len(name) < 5:
        log_message('ERROR: inappropriate name for zip file')
        raise ValueError('Укажите верное имя для архива папки')
    archive_path = Path(name).expanduser()
    parent = archive_path.parent
    if not parent.exists():
        log_message('ERROR: destination folder for zip file does not exist')
        raise FileNotFoundError('Папки сохранения архива не существует')
    if archive_path.suffix.lower() != '.zip':
        log_message('ERROR: inappropriate extension for zip file')
        raise ValueError("Введите имя архива в кавычках с расширением .zip")
    if not path.exists() or path.is_file():
        log_message('ERROR: path is not existing directory')
        raise FileNotFoundError('Такой папки не существует')
    try:
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for child in path.rglob('*'):
                if child.is_file():
                    zf.write(child, arcname=child.relative_to(path))
            print(f"Архив {path} создан в директории {parent}")
            log_message(f"zip {path} -> {archive_path}")
    except PermissionError as p:
        log_message(f'ERROR: zip – permission error {p}')
        print('Недостаточно прав для создания zip-архива для файла')
        raise
    except Exception as e:
        log_message(f'ERROR: zip – exception error {e}')
        raise


def unzip_file(args: list[str]) -> None:
    """
    Распаковывает zip-архив
    :param args: название zip-архива в текущей директории
    :return: None
    """
    if len(args) != 1:
        log_message('ERROR: inappropriate number of unzip arguments')
        raise ValueError('В качестве аргумента к команде unzip укажите только файл для разархивирования')
    path = Path(args[0]).expanduser()
    if path.exists() == False:
        log_message('ERROR: zip archive does not exist')
        raise FileNotFoundError('В текущем каталоге такого архива не существует')
    if path.is_file() == False or path.suffix.lower() != '.zip':
        log_message('ERROR: it is not an archive file')
        raise ValueError('Выбранный файл для разархивирования не является zip архивом')
    try:
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall()
        print(f"Архив {path} распакован в текущую директорию")
        log_message(f"unzip {path}")
    except zipfile.BadZipFile as e:
        log_message(f"ERROR: unzip — bad zip ({e})")
        raise ValueError("Файл не является корректным zip архивом")
    except PermissionError as e:
        log_message(f"ERROR: no permission to unzip ({e})")
        raise PermissionError('Нет прав для разархивирования архива')
    except Exception as e:
        log_message(f"ERROR: something went wrong")
        raise


def tar_folder(args: list[str]) -> None:
    """
    Создает tar.gz-архив указываемой папки
    :param args: список из двух элементов: название папки, название создаваемого архива
    :return: None
    """
    if len(args) != 2:
        log_message('ERROR: not enough arguments')
        raise ValueError('Нужно указать папку и имя архива: tar "<folder>" "<archive.tar.gz>"')
    path = Path(args[0]).expanduser()
    name = args[1]
    if len(name) < 8:
        log_message('ERROR: inappropriate name for tar.gz file')
        raise ValueError('Укажите верное имя для архива папки')
    if not name.lower().endswith(".tar.gz"):
        log_message('ERROR: inappropriate extension for tar.gz file')
        raise ValueError("Введите имя архива в кавычках с расширением .tar.gz")
    archive_path = Path(name).expanduser()
    parent = archive_path.parent
    if not parent.exists():
        log_message('ERROR: destination folder for tar file does not exist')
        raise FileNotFoundError('Папки сохранения архива не существует')
    if not path.exists() or path.is_file():
        log_message('ERROR: path is not existing directory')
        raise FileNotFoundError('Такой папки не существует')
    try:
        with tarfile.open(archive_path, "w:gz") as tf:
            for child in path.rglob("*"):
                tf.add(child, arcname=child.relative_to(path))
            print(f"Архив {path} создан в директории {parent}")
            log_message(f"tar {path} -> {archive_path}")
    except PermissionError as p:
        log_message(f'ERROR: tar.gz – permission error {p}')
        print('Недостаточно прав для создания tar.gz-архива для файла')
        raise
    except Exception as e:
        log_message(f'ERROR: tar – exception error {e}')
        raise


def untar_file(args: list[str]) -> None:
    """
    Распаковывает tar.gz-архив
    :param args: название tar.gz-архива в текущей директории
    :return: None
    """
    if len(args) != 1:
        log_message('ERROR: inappropriate number of untar arguments')
        raise ValueError('В качестве аргумента к команде untar укажите только файл для разархивирования')
    path = Path(args[0]).expanduser()
    if path.exists() == False:
        log_message('ERROR: tar archive does not exist')
        raise FileNotFoundError('В текущем каталоге такого архива не существует')
    if path.is_file() == False or args[0].lower().endswith('.tar.gz') == False:
        log_message('ERROR: it is not an archive-tar file')
        raise ValueError('Выбранный файл для разархивирования не является tar архивом')
    try:
        with tarfile.open(path, "r:gz") as tf:
            tf.extractall()
        print(f"Архив {path} распакован в текущую директорию")
        log_message(f"untar {path}")
    except tarfile.ReadError as e:
        print("Файл не является корректным tar.gz архивом")
        log_message(f"ERROR: untar — bad tar.gz ({e})")
        raise
    except PermissionError as e:
        print("Нет прав для разархивирования архива")
        log_message(f"ERROR: no permission to untar ({e})")
        raise
    except Exception as e:
        log_message("ERROR: something went wrong")
        raise
