from log import log_message
from pathlib import Path
import shutil
import shlex

SHELL_FILE = Path(__file__).resolve().parents[1] / 'shell.log'
TRASH_DIR = Path("/Users/aleksandr/Desktop/python_lab2/.trash")

def undo() -> None:
    """
    Отменяет действие команды из списка cp, mv, rm
    :param: None
    :return: None
    """
    control_str = ""
    with SHELL_FILE.open("r", encoding="utf-8") as s:
        lines = s.readlines()
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            _, rest = line.split("] ", 1)
            if rest.startswith("rm ") or rest.startswith("mv ") or rest.startswith("cp "):
                control_str = rest
                break
    if not control_str:
        print("Нет команд для отката (rm/cp/mv в журнале не найдено)")
        log_message("No rm/mv/cp commands to undo")
        return
    parts = shlex.split(control_str)
    cmd = parts[0]
    if cmd == "rm":
        if '-r' in parts:
            parts.remove('-r')
        name = parts[1]
        idx = parts.index("from")
        original_dir = " ".join(parts[idx + 1:])
        original_dir_path = Path(original_dir)
        src_in_trash = TRASH_DIR / name
        dst_original = original_dir_path

        try:
            shutil.move(src_in_trash, dst_original)
            log_message(f"Undo rm {name} -> {dst_original}")
            print(f"Объект {name} восстановлен в {dst_original}")
        except FileNotFoundError:
            print(f"Не удалось восстановить {name}: файл не найден в корзине {src_in_trash}")
            log_message(f"ERROR: undo rm – file not found in trash ({src_in_trash})")
        except Exception as e:
            print(f"Ошибка при откате rm: {e}")
            log_message(f"ERROR: undo rm failed ({e})")


    elif cmd == "mv":
        src = Path(parts[1]).expanduser()
        dst = Path(parts[2]).expanduser()

        if dst.is_dir():
            real_dst = dst / src.name
        else:
            real_dst = dst
        try:
            shutil.move(real_dst, src)
            log_message(f"Undo mv {dst} -> {src}")
            print(f"Объект возвращён: {dst} → {src}")
        except FileNotFoundError:
            print(f"Не удалось откатить mv: {real_dst} не найден")
            log_message(f"ERROR: undo mv – destination not found ({real_dst})")
        except Exception as e:
            print(f"Ошибка при откате mv: {e}")
            log_message(f"ERROR: undo mv failed ({e})")


    elif cmd == "cp":
        rec = 0
        if "-r" in parts:
            rec = 1
            parts.remove("-r")

        src_str = parts[1]
        dst_str = parts[2]

        src = Path(src_str).expanduser()
        dst = Path(dst_str).expanduser()

        if rec == 0 and dst.is_dir():
            target = dst / src.name
        else:
            target = dst

        if not target.exists():
            print(f"Скопированный объект {target} уже отсутствует, откат невозможен")
            log_message(f"ERROR: undo cp – {target} not exists")
            return
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            log_message(f"Undo cp remove {target}")
            print(f"Копия {target} удалена (откат cp).")

        except Exception as e:
            log_message(f"ERROR: undo cp failed ({e})")
            print(f"Ошибка отката cp: {e}")
            raise