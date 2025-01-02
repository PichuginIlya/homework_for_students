import datetime
import os

from helpers import create_file


class StatsWriter:
    def __init__(self, path: str):
        self.path = path

    def write_metrics(self, metrics: list[tuple[str, str, str]]):
        raise NotImplementedError


class CSVWriter(StatsWriter):
    def write_metrics(self, metrics: list[tuple[str, str, str]]):
        need_header = not os.path.exists(self.path) or os.path.getsize(self.path) == 0
        with open(self.path, "a", encoding="utf-8", newline="") as f:
            if need_header:
                f.write("date;metric;value\n")
            for date_field, name_field, value_field in metrics:
                f.write(f"{date_field};{name_field};{value_field}\n")


class TxtWriter(StatsWriter):
    def write_metrics(self, metrics: list[tuple[str, str, str]]):
        # TXT-формат
        with open(self.path, "a", encoding="utf-8", newline="") as f:
            for date_field, name_field, value_field in metrics:
                f.write(f"{date_field} {name_field} {value_field}\n")
class Statsd:
    def __init__(self, writer: StatsWriter, buffer_limit: int = 10):
        self.writer = writer
        self.buffer_limit = buffer_limit
        self.buffer = []
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.writer.path):
            create_file(self.writer.path)

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
        self.writer.write_metrics(self.buffer)
        self.buffer.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.buffer:
            self._flush()


def get_txt_statsd(path: str, buffer_limit: int = 10) -> Statsd:
    if not path.endswith(".txt"):
        raise ValueError("Файл должен иметь расширение .txt")
    return Statsd(TxtWriter(path), buffer_limit)


def get_csv_statsd(path: str, buffer_limit: int = 10) -> Statsd:
    if not path.endswith(".csv"):
        raise ValueError("Файл должен иметь расширение .csv")
    return Statsd(CSVWriter(path), buffer_limit)
