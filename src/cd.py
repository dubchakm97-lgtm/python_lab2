import os
from log import log_message


def cd(args: list[str]) -> None:
    """
    Меняет текущую директорию
    :param args: список аргументов для cd (path)
    :return: None
    """
    if not args:
        path = os.path.expanduser("~")
        os.chdir(path)
        log_message(f"cd")
    else:
        path = os.path.expanduser(args[0])
    if os.path.exists(path) == False:
        log_message(f"ERROR: path not found ({path})")
        raise FileNotFoundError("Такой папки не существует")
    if not os.path.isdir(path):
        log_message(f"ERROR: not a directory ({path})")
        raise NotADirectoryError("Это не директория")

    try:
        os.chdir(path)
        log_message(f"cd {path}")
        print("Текущая директория:", os.getcwd())
    except Exception as e:
        log_message(f"ERROR: cd failed ({e})")
        print("Ошибка при переходе в директорию:", e)
