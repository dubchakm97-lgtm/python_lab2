import os
import shutil
import logging
from src.log import log_message
from pathlib import Path


def mv(args: list[str]) -> None:
    """
    Перемещает или переименовывает файл или папку
    args: источник копирования, назначение
    return: None
    """
    try:
        if len(args) < 2:
            log_message("mv — missing arguments", logging.WARNING)
            raise ValueError('Укажите исходный и целевой путь!')

        source = os.path.expanduser(args[0])
        destination = os.path.expanduser(args[1])

        if not os.path.exists(source):
            log_message(f"mv — source not found ({source})", logging.WARNING)
            raise FileNotFoundError("Исходный файл или папка не найдены!")

        abs_source = Path(source).resolve()
        abs_destination = Path(destination).resolve(strict=False)

        shutil.move(source, destination)
        log_message(f"mv '{abs_source}' '{abs_destination}'", logging.INFO)
        print(f"Успешно перемещено: {source} → {destination}")

    except Exception as e:
        print("Ошибка при перемещении:", e)
        log_message(f"mv failed ({e})", logging.ERROR)