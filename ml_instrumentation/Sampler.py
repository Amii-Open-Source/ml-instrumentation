import numpy as np
from typing import Callable

class Sampler:
    def next(self, v: float) -> float | None: ...
    def next_eval(self, c: Callable[[], float]) -> float | None: ...
    def end(self) -> float | None: ...

class Ignore:
    def __init__(self): ...
    def next(self, v): return None
    def next_eval(self, v): return None
    def end(self): return None

# by definition, this must be a stateless object
# safe to instantiate a singleton instance for default parameters
ignore = Ignore()

class Identity(Sampler):
    def next(self, v: float):
        return v

    def next_eval(self, c: Callable[[], float]):
        return c()

    def end(self):
        return None

# by definition, this must be a stateless object
# safe to instantiate a singleton instance for default parameters
identity = Identity()

# --------------
# -- Samplers --
# --------------
class Window(Sampler):
    def __init__(self, size: int):
        self._b = np.empty(size, dtype=np.float64)
        self._clock = 0
        self._size = size

    def next(self, v: float):
        self._b[self._clock] = v
        self._clock += 1

        if self._clock == self._size:
            m = self._b.mean()
            self._clock = 0
            return m

    def next_eval(self, c: Callable[[], float]):
        return self.next(c())

    def end(self):
        out = None
        if self._clock > 0:
            out = self._b[:self._clock].mean()

        self._clock = 0
        return out

class Subsample(Sampler):
    def __init__(self, freq: int):
        self._clock = 0
        self._freq = freq

    def next(self, v: float):
        tick = self._clock % self._freq == 0
        self._clock += 1

        if tick:
            return v

    def next_eval(self, c: Callable[[], float]):
        tick = self._clock % self._freq == 0
        self._clock += 1

        if tick:
            return c()

    def end(self):
        self._clock = 0
        return None

class MovingAverage(Sampler):
    def __init__(self, decay: float):
        self._decay = decay
        self.z = 0.

    def next(self, v: float):
        self.z = self._decay * self.z + (1. - self._decay) * v
        return self.z

    def next_eval(self, c: Callable[[], float]):
        v = c()
        return self.next(v)

    def end(self):
        return None
