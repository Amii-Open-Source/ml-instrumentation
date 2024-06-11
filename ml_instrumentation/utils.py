from typing import Callable
from ml_instrumentation.Sampler import Sampler

class Pipe(Sampler):
    def __init__(self, *args: Sampler) -> None:
        self._subs = args

    def next(self, v: float) -> float | None:
        out: float | None = v
        for sub in self._subs:
            if out is None:
                return None
            out = sub.next(out)

        return out

    def next_eval(self, c: Callable[[], float]) -> float | None:
        subs = iter(self._subs)
        first = next(subs)
        out = first.next_eval(c)

        for sub in subs:
            if out is None:
                return None
            out = sub.next(out)

        return out

    def end(self):
        return None
