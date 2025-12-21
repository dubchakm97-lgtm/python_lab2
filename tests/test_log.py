import log
from src.log import log_message

class TestLog:
    def test_log_writes(self):
        log_message("one")
        text = log.LOG_FILE.read_text(encoding="utf-8").strip()
        assert text.startswith("[")
        assert text.endswith(" one")

    def test_log_appends(self):
        log_message("first")
        log_message("second")
        lines = log.LOG_FILE.read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 2
        assert lines[-2].endswith(" first")
        assert lines[-1].endswith(" second")

    def test_log(self):
        msg = "привет"
        log_message(msg)
        content = log.LOG_FILE.read_text(encoding="utf-8")
        assert msg in content