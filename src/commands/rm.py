import os
import shutil
import logging
from src.log import log_message
from pathlib import Path


def rm(args: list[str]) -> None:
    """
    Удаляет файл или папку рекурсивно (с помощью команды -r)
    :param args: может содержать параметр -r, содержит путь
    :return: None
    """
    try:
        if len(args) == 0:
            log_message("rm — no file or directory to remove", logging.WARNING)
            raise ValueError('Укажите файл или каталог для удаления!')

        rec = 0
        if args[0] == '-r':
            rec = 1
            if len(args) < 2:
                log_message("rm — no file or directory to remove", logging.WARNING)
                raise ValueError('Укажите файл или каталог для удаления!')
            path = args[1]
        else:
            path = args[0]

        if path in ['/', '..']:
            log_message(f"rm — forbidden path ({path})", logging.WARNING)
            raise PermissionError('Удаление корневого/родительского каталога запрещено!')

        if not os.path.exists(path):
            log_message(f"rm — path not found ({path})", logging.WARNING)
            raise FileNotFoundError("Такого файла/каталога не существует!")

        destination = Path("/Users/aleksandr/Downloads/python_lab2-main/trash")
        source = Path(path).expanduser().resolve().parent

        if os.path.isfile(path):
            ans = input(f"Удалить '{path}'? (y/n): ").strip().lower()
            if ans != 'y':
                print("Отменено пользователем.")
                log_message(f"rm {('-r ' if rec else '')}{path} — canceled by user", logging.INFO)
            else:
                shutil.move(path, destination)
                print(f"Файл '{path}' успешно удалён.")
                log_message(f"rm '{path}' from '{source}'", logging.INFO)

        elif os.path.isdir(path):
            ans = input(f"Удалить '{path}'? (y/n): ").strip().lower()
            if ans != 'y':
                print("Отменено пользователем.")
                log_message(f"rm {('-r ' if rec else '')}{path} — canceled by user", logging.INFO)
                return
            else:
                if rec == 1:
                    shutil.move(path, destination)
                    print(f"Папка '{path}' успешно удалена из {source}.")
                    log_message(f"rm -r '{path}' from '{source}'", logging.INFO)
                else:
                    log_message(f"rm — directory without -r ({path})", logging.WARNING)
                    raise IsADirectoryError("Это папка, для удаления используйте -r.")

        else:
            log_message(f"rm — unknown type ({path})", logging.WARNING)
            raise OSError("Неизвестный тип объекта.")

    except Exception as e:
        log_message(f"rm failed ({e})", logging.ERROR)
        print("Ошибка при удалении: ", e)