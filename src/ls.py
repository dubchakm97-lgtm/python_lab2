import os
import datetime
from log import log_message


def ls(args: list[str]) -> None:
    """
    Выводит содержимое текущей директории, при команде -l делает подробный вывод
    :param args: аргументы команды ls (-l, путь)
    :return: None
    """
    path = "."
    long = 0
    for a in args:
        if a == "-l":
            long = 1
        else:
            path = os.path.expanduser(a)

    if os.path.exists(path) == False:
        log_message(f"ERROR: path not found ({path})")
        raise FileNotFoundError("Такой папки не существует")

    if os.path.isfile(path):
        if long == 1:
            st = os.stat(path)
            size = st.st_size
            mtime = datetime.datetime.fromtimestamp(st.st_mtime)
            print(f"{path} \t{size} bytes\t{mtime}")
        else:
            print(path)
        log_message(f"ls {' '.join(args)}")
        return

    try:
        items = os.listdir(path)
        for item in items:
            full_path = os.path.join(path, item)
            if long == 1:
                st = os.stat(full_path)
                size = st.st_size
                mtime = datetime.datetime.fromtimestamp(st.st_mtime)
                print(f"{item} \t{size} bytes\t{mtime}")
            else:
                print(item)
        log_message(f"ls {' '.join(args)}")

    except Exception as e:
        log_message(f"ERROR: ls failed ({e})")
        raise