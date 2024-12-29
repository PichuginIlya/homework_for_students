from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def chain(*iterables: Iterable[T]) -> Generator[T, None, None]:
    for it in iterables:
        for item in it:
            yield item


class Chain:
    def __init__(self, *iterables: Iterable[T]):
        self.iterables = iterables
        self.current_iterator = iter(self.iterables)
        self.inner_iterator = iter(next(self.current_iterator))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.inner_iterator)
        except StopIteration:
            try:
                self.inner_iterator = iter(next(self.current_iterator))
                return next(self.inner_iterator)
            except StopIteration:
                raise StopIteration
