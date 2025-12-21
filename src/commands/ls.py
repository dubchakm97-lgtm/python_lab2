import os
import datetime
import logging
from src.log import log_message


def has_xattr(p: str, ext: int) -> bool:
    if ext == 0:
        return False
    try:
        return len(os.listxattr(p)) > 0
    except Exception:
        return False


def ls(args: list[str]) -> None:
    """
    Выводит содержимое директории/файлов.
    Флаги:
    -l - подробный вывод
    -a - показывать скрытые (начинаются с '.')
    -e - показывать индикатор расширенных атрибутов (@) если есть
    Поддерживаются комбинации: -le, -ae, -lae, -a, -e, -l, -la.
    При нескольких путях выводит каждый.
    """
    try:
        long = 0
        hide = 0
        ext = 0
        paths = []

        for a in args:
            if a.startswith("-") and a != "-":
                flags = a[1:]
                for ch in flags:
                    if ch == "l":
                        long = 1
                    elif ch == "a":
                        hide = 1
                    elif ch == "e":
                        ext = 1
                    else:
                        log_message(f"ls — unknown flag ({a})", logging.WARNING)
                        raise ValueError(f"Неизвестный флаг: -{ch}")
            else:
                paths.append(os.path.expanduser(a))

        if not paths:
            paths = ["."]
        multi = len(paths) > 1

        for path in paths:
            if not os.path.exists(path):
                log_message(f"ls — path not found ({path})", logging.WARNING)
                print(f"ls: cannot access '{path}': No such file or directory")
                continue

            if multi:
                print(f"{path}:")

            if os.path.isfile(path):
                mark = "@" if has_xattr(path, ext) else ""
                if long:
                    st = os.stat(path)
                    size = st.st_size
                    mtime = datetime.datetime.fromtimestamp(st.st_mtime)
                    print(f"{path}{mark}\t{size} bytes\t{mtime}")
                else:
                    print(f"{path}{mark}")
            else:
                items = sorted(os.listdir(path))

                if not hide:
                    items = [x for x in items if not x.startswith(".")]

                for item in items:
                    full_path = os.path.join(path, item)
                    mark = "@" if has_xattr(full_path, ext) else ""

                    if long:
                        st = os.stat(full_path)
                        size = st.st_size
                        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
                        print(f"{item}{mark}\t{size} bytes\t{mtime}")
                    else:
                        print(f"{item}{mark}")

            if multi:
                print()

        log_message(f"ls {' '.join(args)}", logging.INFO)

    except Exception as e:
        log_message(f"ls failed ({e})", logging.ERROR)
        print("Ошибка при выводе содержимого: ", e)