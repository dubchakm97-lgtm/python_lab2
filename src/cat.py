import os
from log import log_message


def cat(args: list[str]) -> None:
    """
    Выводит содержимое указанного файла
    :param args: путь к файлу
    :return: None
    """
    if not args:
        log_message(f'ERROR: cat — no file specified')
        raise ValueError('Ошибка! Не указан файл!')
    path = os.path.expanduser(args[0])
    if os.path.exists(path) == False:
        log_message(f"ERROR: file not found ({path})")
        raise FileNotFoundError('Ошибка! Такого файла не существует!')
    if os.path.isfile(path) == False:
        log_message(f"ERROR: not a file ({path})")
        raise IsADirectoryError("Ошибка! это не файл!")
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
            log_message(f"cat {path}")
    except Exception as e:
        print("Ошибка при чтении файла:", e)
        log_message(f"ERROR: cat failed ({e})")