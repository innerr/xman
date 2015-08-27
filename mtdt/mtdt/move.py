import math

class Move:
    def __init__(self, rg = 8, peace = 64, still = 4, power = 1600):
        self._rg = rg
        self._peace = peace
        self._still = still
        self._power = power

        self._i = 0

    def on(self, i, v, d):
        if i < self._i + self._rg:
            return

        d = d[-self._rg:]

        a = 0
        b = 0
        for n in d:
            a += n
            b += abs(n)
        if abs(a) > self._peace:
            return

        if b < self._power:
            return
        for n in d[-1:]:
            if n > self._still:
                return

        self._i = i
        return abs(a)
