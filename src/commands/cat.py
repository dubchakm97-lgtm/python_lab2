import os
import logging
from src.log import log_message


def cat(args: list[str]) -> None:
    """
    Выводит содержимое указанного файла
    :param args: путь к файлу
    :return: None
    """
    try:
        if not args:
            log_message("cat — no file specified", logging.WARNING)
            raise ValueError('Не указан файл!')

        path = os.path.expanduser(args[0])

        if os.path.exists(path) == False:
            log_message(f"cat — file not found ({path})", logging.WARNING)
            raise FileNotFoundError('Такого файла не существует!')

        if os.path.isfile(path) == False:
            log_message(f"cat — not a file ({path})", logging.WARNING)
            raise IsADirectoryError("Это не файл!")

        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
            log_message(f"cat {path}", logging.INFO)

    except Exception as e:
        print("Ошибка при чтении файла:", e)
        log_message(f"cat failed ({e})", logging.ERROR)