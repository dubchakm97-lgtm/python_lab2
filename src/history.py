from log import log_message
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parents[1] / '.history.txt'

def history(args: list[str]) -> None:
    """
    Выводит последние напечатанные команды из .history.txt, куда записываются
    все команды, вводимые с клавиатуры
    :param args: количество выводимых команд
    :return: None
    """
    if len(args) != 1:
        log_message('ERROR: wrong amount of history arguments')
        raise ValueError('Введите команду history с указанием количества последних введённых команд')

    try:
        arg = int(args[0])
    except ValueError:
        log_message('ERROR: wrong amount/type of history arguments')
        raise ValueError('Введите команду history с указанием количества последних введённых команд')

    if arg <= 0:
        log_message('ERROR: wrong amount of history arguments')
        raise ValueError('Введите команду history с указанием натурального количества последних введённых команд')

    with HISTORY_FILE.open('r', encoding="utf-8") as h:
        lines = h.readlines()
        if arg > len(lines):
            log_message('ERROR: not enough strings in history.txt')
            raise ValueError('Количество введенных ранее команд меньше')
        for string in range(len(lines)-1, -1, -1):
            if arg == 0:
                break
            print(lines[string], end="")
            arg -= 1