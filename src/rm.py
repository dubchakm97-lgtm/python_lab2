import os
import shutil
from log import log_message
from pathlib import Path


def rm(args: list[str]) -> None:
    """
    Удаляет файл или папку рекурсивно (с помощью команды -r)
    :param args: может содержать параметр -r, содержит путь
    :return: None
    """
    if len(args) == 0:
        log_message('ERROR: rm — no file or directory to remove')
        raise ValueError('Укажите файл или каталог для удаления!')
    rec = 0
    if args[0] == '-r':
        rec = 1
        if len(args) < 2:
            log_message(f'ERROR: rm — no file or directory to remove')
            raise ValueError('Укажите файл или каталог для удаления!')
        path = args[1]
    else:
        path = args[0]

    if path in ['/', '..']:
        log_message(f"ERROR: impossible to remove ({path})")
        raise PermissionError('Удаление корневого/родительского каталога запрещено!')

    if not os.path.exists(path):
        log_message(f"ERROR: path/folder not found ({path})")
        raise FileNotFoundError("Такого файла/каталога не существует!")
    destination = Path("/Users/aleksandr/Desktop/python_lab2/.trash")
    source = Path(path).expanduser().resolve().parent
    try:
        if os.path.isfile(path):
            ans = input(f"Удалить '{path}'? (y/n): ").strip().lower()
            if ans != 'y':
                print("Отменено пользователем.")
                log_message(f"rm {('-r ' if rec else '')}{path} — canceled by user")
            else:
                shutil.move(path, destination)
                print(f"Файл '{path}' успешно удалён.")
                log_message(f"rm '{path}' from '{source}'")
        elif os.path.isdir(path):
            ans = input(f"Удалить '{path}'? (y/n): ").strip().lower()
            if ans != 'y':
                print("Отменено пользователем.")
                log_message(f"rm {('-r ' if rec else '')}{path} — canceled by user")
                return 0
            else:
                if rec == 1:
                    shutil.move(path, destination)
                    print(f"Папка '{path}' успешно удалена из {source}.")
                    log_message(f"rm -r '{path}' from '{source}'")
                else:
                    log_message(f"ERROR: rm — directory without -r ({path})")
                    raise IsADirectoryError("Это папка, для удаления используйте -r.")
        else:
            log_message(f"ERROR: rm — unknown type ({path})")
            raise OSError("Неизвестный тип объекта.")
    except Exception as e:
        log_message(f"ERROR: rm failed ({e})")
        raise
