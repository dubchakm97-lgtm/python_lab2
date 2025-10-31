from ls import ls
from cd import cd
from cat import cat
from cp import cp
from mv import mv
from rm import rm
from log import log_message


def main() -> None:
    """
    Основной цикл работы программы, принимает на вход команды от пользователя, вызывает функции-команды
    :return: None
    """
    while True:
        try:
            line = input('$ ')
            parts = line.split()
            main_p = parts[0]
            args = parts[1:]

            if main_p == "ls":
                ls(args)
            elif main_p == "cd":
                cd(args)
            elif main_p == "cat":
                cat(args)
            elif main_p == "cp":
                cp(args)
            elif main_p == "mv":
                mv(args)
            elif main_p == "rm":
                rm(args)
            elif main_p in ['exit', "quit"]:
                break
            else:
                log_message(f'ERROR: unknown command {main_p}')
                print(f"Неизвестная команда {main_p}")
        except (FileNotFoundError, NotADirectoryError, IsADirectoryError, PermissionError, ValueError, OSError) as e:
            print(f'Ошибка! {e}')


if __name__ == '__main__':
    main()
