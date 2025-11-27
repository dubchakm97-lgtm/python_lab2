from log import log_message
from pathlib import Path


def grep(args: list[str]) -> None:
    if '-i' not in args and '-r' not in args and '-ri' not in args:
        if len(args) != 2:
            log_message('ERROR: inappropriate amount of grep arguments')
            raise ValueError('Введите искомую строку и файл для поиска')
        string = args[0]
        destination = Path(args[1]).expanduser()
        if not destination.exists():
            log_message('ERROR: file does not exist')
            raise FileNotFoundError('Файла не существует в этой директории')
        if destination.is_dir():
            log_message('ERROR: grep folder without -r')
            raise IsADirectoryError('Для поиска строки в файлах папки используйте флаг -r')
        try:
            with destination.open('r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                count = 1
                for row in lines:
                    if string in row:
                        print(f'{destination}; {count}: {row.rstrip()}')
                        log_message(f"grep match '{string}' in {destination}:{count}")
                    count += 1
        except PermissionError:
            log_message('ERROR: no rights to read the file')
            raise PermissionError('Недостаточно прав для прочтения файла')
        except Exception:
            log_message('ERROR: something went wrong')
            raise Exception("Something went wrong")
    elif '-i' in args and '-r' not in args:
        if len(args) != 3:
            log_message('ERROR: inappropriate amount of grep arguments')
            raise ValueError('Введите искомую строку, файл и флаг -i для поиска')
        flag = '-i'
        args.remove(flag)
        string = args[0]
        destination = Path(args[1]).expanduser()
        if not destination.exists():
            log_message('ERROR: file does not exist')
            raise FileNotFoundError('Файла не существует в этой директории')
        if destination.is_dir():
            log_message('ERROR: grep folder without -r')
            raise IsADirectoryError('Для поиска строки в файлах папки используйте флаг -r')
        try:
            with destination.open('r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                count = 1
                for row in lines:
                    if string.lower() in row.lower():
                        print(f'{destination}; {count}: {row.rstrip()}')
                        log_message(f"grep -i match '{string}' in {destination}:{count}")
                    count += 1
        except PermissionError:
            log_message('ERROR: no rights to read the file')
            raise PermissionError('Недостаточно прав для прочтения файла')
        except Exception:
            log_message('ERROR: something went wrong')
            raise Exception("Something went wrong")
    elif '-r' in args and '-i' not in args:
        if len(args) != 3:
            log_message('ERROR: inappropriate amount of grep arguments')
            raise ValueError('Введите искомую строку, папку и флаг -r для поиска')
        flag = '-r'
        args.remove(flag)
        string = args[0]
        destination = Path(args[1]).expanduser()
        if not destination.exists():
            log_message('ERROR: folder does not exist')
            raise FileNotFoundError('Папки не существует в этой директории')
        if destination.is_file():
            log_message('ERROR: grep file with -r')
            raise ValueError('Для поиска строки в файле не используйте флаг -r')
        try:
            for file in destination.rglob('*'):
                if file.is_file():
                    with file.open('r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = 1
                        for row in lines:
                            if string in row:
                                print(f'{file}; {count}: {row.rstrip()}')
                                log_message(f"grep match -r '{string}' in {file}:{count}")
                            count += 1
        except PermissionError:
            log_message('ERROR: no permission to read a file/open the folder')
            raise PermissionError('Недостаточно прав для чтения файла/открытия папки')
        except Exception as e:
            log_message('ERROR: something went wrong')
            raise Exception(f'Something went wrong: {e}')
    else:
        if len(args) != 3:
            log_message('ERROR: inappropriate amount of grep arguments')
            raise ValueError('Введите искомую строку, папку и флаг -ri для регистронезависимого поиска')
        flag = '-ri'
        args.remove(flag)
        string = args[0]
        destination = Path(args[1]).expanduser()
        if not destination.exists():
            log_message('ERROR: folder does not exist')
            raise FileNotFoundError('Папки не существует в этой директории')
        if destination.is_file():
            log_message('ERROR: grep file with -ri')
            raise ValueError('Для поиска строки в файле не используйте флаг -ri')
        try:
            for file in destination.rglob('*'):
                if file.is_file():
                    with file.open('r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = 1
                        for row in lines:
                            if string.lower() in row.lower():
                                print(f'{file}; {count}: {row.rstrip()}')
                                log_message(f"grep match -ri '{string}' in {file}:{count}")
                            count += 1
        except PermissionError:
            log_message('ERROR: no permission to read a file/open the folder')
            raise PermissionError('Недостаточно прав для чтения файла/открытия папки')
        except Exception as e:
            log_message('ERROR: something went wrong')
            raise Exception(f'Something went wrong: {e}')
