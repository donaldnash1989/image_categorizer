from ..interfaces.logger import ILogger

class ConsoleLogger(ILogger):
    def info(self, msg: str) -> None:
        print(f"[INFO] {msg}")
    def warn(self, msg: str) -> None:
        print(f"[WARN] {msg}")
    def error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")
