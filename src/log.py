import logging
from src.constants import LOG_FILE

_logger = None


def _get_logger() -> logging.Logger:
    global _logger
    if _logger is not None:
        return _logger

    logger = logging.getLogger("shell")
    logger.setLevel(logging.INFO)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8", delay=False)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    _logger = logger
    return logger

def log_message(text: str, level: int = logging.INFO) -> None:
    """
    Добавляет запись исполнения команды или ошибки в журнал shell.log
    :param text: запись команды/ошибки
    :return: None
    """
    logger = _get_logger()
    logger.log(level, text)
