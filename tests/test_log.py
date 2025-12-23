import logging
from unittest.mock import patch
import src.log as log


def _reset_shell_logger():
    log._logger = None
    lg = logging.getLogger("shell")
    for h in list(lg.handlers):
        lg.removeHandler(h)


class TestLog:
    def test_log_writes_line(self, tmp_path):
        lf = tmp_path / "shell.log"

        _reset_shell_logger()
        with patch.object(log, "LOG_FILE", lf, create=True):
            log.log_message("one")

        text = lf.read_text(encoding="utf-8")
        assert " INFO " in text
        assert text.rstrip().endswith(" one")

    def test_log_appends_and_levels(self, tmp_path):
        lf = tmp_path / "shell.log"

        _reset_shell_logger()
        with patch.object(log, "LOG_FILE", lf, create=True):
            log.log_message("first")
            log.log_message("second", level=logging.ERROR)

        lines = lf.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        assert " INFO " in lines[0] and lines[0].endswith(" first")
        assert " ERROR " in lines[1] and lines[1].endswith(" second")