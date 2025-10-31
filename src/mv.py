import os
import shutil
from log import log_message


def mv(args: list[str]) -> None:
    """
    Перемещает или переименовывает файл или папку
    args: источник копирования, назначение
    return: None
    """
    if len(args) < 2:
        log_message('ERROR: mv — missing arguments')
        raise ValueError('Ошибка! Укажите исходный и целевой путь!')
    source = os.path.expanduser(args[0])
    destination = os.path.expanduser(args[1])
    if not os.path.exists(source):
        log_message(f"ERROR: mv — source not found ({source})")
        raise FileNotFoundError("Ошибка! Исходный файл или папка не найдены!")
    try:
        shutil.move(source, destination)
        log_message(f"mv {source} {destination}")
        print(f"Успешно перемещено: {source} → {destination}")
    except Exception as e:
        print("Ошибка при перемещении:", e)
        log_message(f"ERROR: mv failed ({e})")