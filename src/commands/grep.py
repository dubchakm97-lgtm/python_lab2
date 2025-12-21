import logging
from src.log import log_message
from pathlib import Path


def grep(args: list[str]) -> None:
    """
    Поиск строки по содержимому файла/файлов папки
    :param args: искомая строка/подстрока, название файла/папки с файлами
    :return: None
    """
    if '-i' not in args and '-r' not in args and '-ri' not in args:
        try:
            if len(args) != 2:
                log_message("grep — inappropriate amount of arguments", logging.WARNING)
                raise ValueError('Введите искомую строку и файл для поиска')

            string = args[0]
            destination = Path(args[1]).expanduser()

            if not destination.exists():
                log_message("grep — file does not exist", logging.WARNING)
                raise FileNotFoundError('Файла не существует в этой директории')

            if destination.is_dir():
                log_message("grep — folder without -r", logging.WARNING)
                raise IsADirectoryError('Для поиска строки в файлах папки используйте флаг -r')

            with destination.open('r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                count = 1
                for row in lines:
                    if string in row:
                        print(f'{destination}; {count}: {row.rstrip()}')
                        log_message(f"grep match '{string}' in {destination}:{count}", logging.INFO)
                    count += 1

        except PermissionError:
            log_message("grep — no rights to read the file", logging.ERROR)
            print('Недостаточно прав для прочтения файла')
        except Exception as e:
            log_message(f"grep failed ({e})", logging.ERROR)
            print("Something went wrong")

    elif '-i' in args and '-r' not in args:
        try:
            if len(args) != 3:
                log_message("grep -i — inappropriate amount of arguments", logging.WARNING)
                raise ValueError('Введите искомую строку, файл и флаг -i для поиска')

            flag = '-i'
            args.remove(flag)
            string = args[0]
            destination = Path(args[1]).expanduser()

            if not destination.exists():
                log_message("grep -i — file does not exist", logging.WARNING)
                raise FileNotFoundError('Файла не существует в этой директории')

            if destination.is_dir():
                log_message("grep -i — folder without -r", logging.WARNING)
                raise IsADirectoryError('Для поиска строки в файлах папки используйте флаг -r')

            with destination.open('r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                count = 1
                for row in lines:
                    if string.lower() in row.lower():
                        print(f'{destination}; {count}: {row.rstrip()}')
                        log_message(f"grep -i match '{string}' in {destination}:{count}", logging.INFO)
                    count += 1

        except PermissionError:
            log_message("grep -i — no rights to read the file", logging.ERROR)
            print('Недостаточно прав для прочтения файла')
        except Exception as e:
            log_message(f"grep -i failed ({e})", logging.ERROR)
            print("Something went wrong")

    elif '-r' in args and '-i' not in args:
        try:
            if len(args) != 3:
                log_message("grep -r — inappropriate amount of arguments", logging.WARNING)
                raise ValueError('Введите искомую строку, папку и флаг -r для поиска')

            flag = '-r'
            args.remove(flag)
            string = args[0]
            destination = Path(args[1]).expanduser()

            if not destination.exists():
                log_message("grep -r — folder does not exist", logging.WARNING)
                raise FileNotFoundError('Папки не существует в этой директории')

            if destination.is_file():
                log_message("grep -r — file with -r", logging.WARNING)
                raise ValueError('Для поиска строки в файле не используйте флаг -r')

            for file in destination.rglob('*'):
                if file.is_file():
                    with file.open('r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = 1
                        for row in lines:
                            if string in row:
                                print(f'{file}; {count}: {row.rstrip()}')
                                log_message(f"grep -r match '{string}' in {file}:{count}", logging.INFO)
                            count += 1

        except PermissionError:
            log_message("grep -r — no permission to read/open", logging.ERROR)
            print('Недостаточно прав для чтения файла/открытия папки')
        except Exception as e:
            log_message(f"grep -r failed ({e})", logging.ERROR)
            print(f'Something went wrong: {e}')

    else:
        try:
            if len(args) != 3:
                log_message("grep -ri — inappropriate amount of arguments", logging.WARNING)
                raise ValueError('Введите искомую строку, папку и флаг -ri для регистронезависимого поиска')

            flag = '-ri'
            args.remove(flag)
            string = args[0]
            destination = Path(args[1]).expanduser()

            if not destination.exists():
                log_message("grep -ri — folder does not exist", logging.WARNING)
                raise FileNotFoundError('Папки не существует в этой директории')

            if destination.is_file():
                log_message("grep -ri — file with -ri", logging.WARNING)
                raise ValueError('Для поиска строки в файле не используйте флаг -ri')

            for file in destination.rglob('*'):
                if file.is_file():
                    with file.open('r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = 1
                        for row in lines:
                            if string.lower() in row.lower():
                                print(f'{file}; {count}: {row.rstrip()}')
                                log_message(f"grep -ri match '{string}' in {file}:{count}", logging.INFO)
                            count += 1

        except PermissionError:
            log_message("grep -ri — no permission to read/open", logging.ERROR)
            print('Недостаточно прав для чтения файла/открытия папки')
        except Exception as e:
            log_message(f"grep -ri failed ({e})", logging.ERROR)
            print(f'Something went wrong: {e}')