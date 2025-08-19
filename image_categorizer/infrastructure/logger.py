from ..interfaces.logger import ILogger
import sys


def _open_log_file(path: str):
    """Open a log file for writing when no console is available."""
    return open(path, "a", encoding="utf-8")

class ConsoleLogger(ILogger):
    def __init__(self, log_path: str = "app.log") -> None:
        self._stdout = sys.stdout
        self._log_file = None if self._stdout else _open_log_file(log_path)

    def _write(self, level: str, msg: str) -> None:
        formatted = f"[{level}] {msg}\n"
        if self._stdout:
            self._stdout.write(formatted)
            self._stdout.flush()
        else:
            self._log_file.write(formatted)
            self._log_file.flush()

    def info(self, msg: str) -> None:
        self._write("INFO", msg)

    def warn(self, msg: str) -> None:
        self._write("WARN", msg)

    def error(self, msg: str) -> None:
        self._write("ERROR", msg)
