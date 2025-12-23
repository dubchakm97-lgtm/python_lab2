import logging
from src.log import log_message
from src.constants import HISTORY_FILE


def history(args: list[str]) -> None:
    """
    Выводит последние напечатанные команды из .history.txt, куда записываются
    все команды, вводимые с клавиатуры
    :param args: количество выводимых команд
    :return: None
    """
    if len(args) != 1:
        log_message("history — wrong amount of arguments", logging.WARNING)
        raise ValueError('Введите команду history с указанием количества последних введённых команд')

    try:
        arg = int(args[0])

        if arg <= 0:
            log_message("history — non-positive amount", logging.WARNING)
            raise ValueError('Введите команду history с указанием натурального количества последних введённых команд')

        with HISTORY_FILE.open('r', encoding="utf-8") as h:
            lines = h.readlines()

            if arg > len(lines):
                log_message("history — not enough lines in history file", logging.WARNING)
                raise ValueError('Количество введенных ранее команд меньше')

            for string in range(len(lines) - 1, -1, -1):
                if arg == 0:
                    break
                print(lines[string], end="")
                arg -= 1

        log_message(f"history {args[0]}", logging.INFO)

    except ValueError:
        log_message("history — wrong amount/type of arguments", logging.WARNING)
        print(
            'Введите команду history с указанием количества последних введённых команд, не превышающего количество ранее введенных команд')
