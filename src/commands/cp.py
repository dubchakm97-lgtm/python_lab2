import shutil
import pathlib
import logging
from src.log import log_message


def cp(args: list[str]) -> None:
    """
    Копирует файл или папку
    :param args: источник копирования, назначение
    :return: None
    """
    try:
        arg = []
        pointer = 0
        for a in args:
            if a == '-r':
                pointer = 1
            else:
                arg.append(a)

        if len(arg) != 2:
            log_message("cp — not enough arguments", logging.WARNING)
            raise ValueError("Нужно указать источник и назначение")

        source = pathlib.Path(arg[0]).expanduser().resolve()
        direction = pathlib.Path(arg[1]).expanduser().resolve()

        if not source.exists():
            log_message(f"cp — source not found ({source})", logging.WARNING)
            raise FileNotFoundError("Источник не найден!")

        if source.is_dir():
            if pointer == 0:
                log_message("cp — use -r to copy folder", logging.WARNING)
                raise IsADirectoryError('Используйте -r для копирования папки')

            if direction.exists() and direction.is_dir():
                real_dst = direction / source.name
            else:
                real_dst = direction

            shutil.copytree(source, real_dst, dirs_exist_ok=True)
            log_message(f"cp -r '{source}' '{real_dst}'", logging.INFO)

        else:
            shutil.copy2(source, direction)
            log_message(f"cp '{source}' '{direction}'", logging.INFO)

        print(f"Скопировано: {source} → {direction}")

    except Exception as e:
        log_message(f"cp failed ({e})", logging.ERROR)
        print("Ошибка при копировании: ", e)