import os
import logging
from src.log import log_message


def cd(args: list[str]) -> None:
    """
    Меняет текущую директорию
    :param args: список аргументов для cd (path)
    :return: None
    """
    try:
        if not args:
            path = os.path.expanduser("~")
            os.chdir(path)
            log_message("cd", logging.INFO)
        else:
            path = os.path.expanduser(args[0])

        if os.path.exists(path) == False:
            log_message(f"cd — path not found ({path})", logging.WARNING)
            raise FileNotFoundError("Такой папки не существует")

        if not os.path.isdir(path):
            log_message(f"cd — not a directory ({path})", logging.WARNING)
            raise NotADirectoryError("Это не директория")

        os.chdir(path)
        log_message(f"cd {path}", logging.INFO)
        print("Текущая директория:", os.getcwd())

    except Exception as e:
        log_message(f"cd failed ({e})", logging.ERROR)
        print("Ошибка при переходе в директорию:", e)