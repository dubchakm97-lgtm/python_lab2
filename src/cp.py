import shutil
import pathlib
from log import log_message


def cp(args: list[str]) -> None:
    """
    Копирует файл или папку
    :param args: источник копирования, назначение
    :return: None
    """
    arg = []
    pointer = 0
    for a in args:
        if a == '-r':
            pointer = 1
        else:
            arg.append(a)
    if len(arg) != 2:
        log_message("ERROR: cp — not enough arguments")
        raise ValueError("Ошибка: нужно указать источник и назначение")
    source = pathlib.Path(arg[0]).expanduser()
    direction = pathlib.Path(arg[1]).expanduser()
    if not source.exists():
        log_message(f"ERROR: cp — source not found ({source})")
        raise FileNotFoundError("Ошибка! Источник не найден!")
    try:
        if source.is_dir():
            if pointer == 0:
                log_message(f'ERROR: use -r to copy folder')
                raise IsADirectoryError('Ошибка! Используйте -r для копирования папки')
            shutil.copytree(source, direction, dirs_exist_ok=True)
        else:
            shutil.copy2(source, direction)
        print(f"Скопировано: {source} → {direction}")
        log_message(f"cp {source} {direction}")
    except Exception as e:
        log_message(f"ERROR: cp failed ({e})")
        raise
