from ls import ls
from cd import cd
from cat import cat
from cp import cp
from mv import mv
from rm import rm
from log import log_message
from pathlib import Path
from history import history
from command_undo import undo
from archives import zip_folder, unzip_file, tar_folder, untar_file
import shlex
from grep import grep


HISTORY_FILE = Path(__file__).resolve().parents[1] / '.history.txt'

def main() -> None:
    """
    Основной цикл работы программы, принимает на вход команды от пользователя, вызывает функции-команды
    :return: None
    """
    while True:
        with HISTORY_FILE.open('r', encoding='utf-8') as h:
            lines = h.readlines()
            for row in lines:
                if len(row) != 0:
                    count_of_commands = ''
                    for alp in lines[-1]:
                        if alp.isdigit()==True:
                            count_of_commands += alp
                        else:
                            break
                    count_of_commands = int(count_of_commands) + 1
                    break
            else:
                count_of_commands = 1
        try:
            line = input('$ ')
            parts = line.split()
            if len(parts) == 0:
                print('Введите команду')
                log_message('ERROR: no command was there')
                with HISTORY_FILE.open('a', encoding='utf-8') as h:
                    h.write(f'{count_of_commands}: *no command*\n')
                continue
            main_p = parts[0]
            args = parts[1:]
            if main_p == "ls":
                ls(shlex.split(' '.join(args)))
            elif main_p == "cd":
                cd(shlex.split(' '.join(args)))
            elif main_p == "cat":
                cat(shlex.split(' '.join(args)))
            elif main_p == "cp":
                cp(shlex.split(' '.join(args)))
            elif main_p == "mv":
                mv(shlex.split(' '.join(args)))
            elif main_p == "rm":
                rm(shlex.split(' '.join(args)))
            elif main_p == "undo":
                undo()
            elif main_p == "history":
                history(shlex.split(' '.join(args)))
            elif main_p == "zip":
                zip_folder(shlex.split(' '.join(args)))
            elif main_p == "unzip":
                unzip_file(shlex.split(' '.join(args)))
            elif main_p == "tar":
                tar_folder(shlex.split(' '.join(args)))
            elif main_p == "untar":
                untar_file(shlex.split(' '.join(args)))
            elif main_p == "grep":
                grep(shlex.split(' '.join(args)))
            elif main_p in ['exit', "quit"]:
                break
            else:
                log_message(f'ERROR: unknown command {main_p}')
                print(f"Неизвестная команда {main_p}")
            with HISTORY_FILE.open('a', encoding='utf-8') as h:
                h.write(f'{count_of_commands}: {main_p} {shlex.split(' '.join(args))}\n')
        except (FileNotFoundError, NotADirectoryError, IsADirectoryError, PermissionError, ValueError, OSError, Exception) as e:
            print(f'Ошибка! {e}')


if __name__ == '__main__':
    main()
