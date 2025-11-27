# from pathlib import Path
# import logging
#
# LOG_FILE = Path(__file__).resolve().parents[1] / "shell.log"
#
# logger = logging.getLogger("shell")
# logger.setLevel(logging.INFO)
#
#
# if not logger.handlers:
#     LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
#     file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
#     formatter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="[%Y-%m-%d %H:%M:%S]")
#     file_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
#     logger.propagate = False
#
#
# def log_message(text: str, level: str = 'info') -> None:
#     """
#     Добавляет запись исполнения команды или ошибки в журнал shell.log
#     :param text: запись команды/ошибки
#     :param level: уровень сообщения в лог (если не передать второй аргумент при записи в лог,
#     он автоматически равен 'info')
#     :return: None
#     """
#     if level == "error":
#         logger.error(text)
#     else:
#         logger.info(text)



import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parents[1] / "shell.log"


def log_message(text: str) -> None:
    """
    Добавляет запись исполнения команды или ошибки в журнал shell.log
    :param text: запись команды/ошибки
    :return: None
    """
    now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{now} {text}\n")