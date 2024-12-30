from typing import Generator, Iterable, TypeVar, Iterator

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
    def __init__(self, iterable: Iterable[T]):
        self.iterable = iterable
        self.saved = list(iterable)  
        self.iterator = iter(self.saved)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        try:
            return next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.saved)
            return next(self.iterator)