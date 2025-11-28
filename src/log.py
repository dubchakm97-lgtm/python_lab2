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