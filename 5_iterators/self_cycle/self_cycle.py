from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def cycle(obj: Iterable[T]) -> Generator[T, None, None]:
    saved = []
    for item in obj:
        yield item
        saved.append(item)
    while saved:
        for item in saved:
            yield item


class Cycle:
    def __init__(self, obj: Iterable[T]):
        self.obj = obj
        self.saved = []
        self.iterator = iter(obj)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = next(self.iterator)
            self.saved.append(item)
            return item
        except StopIteration:
            self.iterator = iter(self.saved)
            return next(self.iterator)