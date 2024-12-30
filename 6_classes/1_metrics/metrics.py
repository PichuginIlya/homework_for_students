import os
import datetime
from helpers import create_file


class Statsd:
    def __init__(self, path: str, buffer_limit: int = 10):
        self.path = path
        self.buffer_limit = buffer_limit
        self.buffer = []
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.splitext(self.path)[1]:
            return
        if not os.path.exists(self.path):
            create_file(self.path)

    def incr(self, name: str, value: int = 1):
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        self.buffer.append((now, name, str(value)))
        if len(self.buffer) >= self.buffer_limit:
            self._flush()

    def decr(self, name: str, value: int = 1):
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        self.buffer.append((now, name, str(-value)))
        if len(self.buffer) >= self.buffer_limit:
            self._flush()

    def _flush(self):
        need_header = not os.path.exists(self.path) or os.path.getsize(self.path) == 0
        with open(self.path, "a", encoding="utf-8", newline="") as f:
            if need_header:
                if self.path.endswith(".csv"):
                    f.write("date;metric;value\n")

            for date_field, name_field, value_field in self.buffer:
                if self.path.endswith(".csv"):
                    f.write(f"{date_field};{name_field};{value_field}\n")
                else:
                    f.write(f"{date_field} {name_field} {value_field}\n")

        self.buffer.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.buffer:
            self._flush()


def get_txt_statsd(path: str, buffer_limit: int = 10) -> Statsd:
    if not path.endswith(".txt"):
        raise ValueError("Файл должен иметь расширение .txt")
    return Statsd(path, buffer_limit)


def get_csv_statsd(path: str, buffer_limit: int = 10) -> Statsd:
    if not path.endswith(".csv"):
        raise ValueError("Файл должен иметь расширение .csv")
    return Statsd(path, buffer_limit)