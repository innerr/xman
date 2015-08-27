import math

class Punch:
    def __init__(self, weight = 256, burstiness = 2):
        self._weight = weight
        self._burstiness = burstiness
        self._w = 0

    def on(self, i, v, d):
        if self._w > 0 and d[-1] <= 0:
            w, self._w = self._w, 0
            return int(math.sqrt(w))
        for j in range(0, self._burstiness):
            n = d[-1 - j]
            if 0 < n and n < self._weight:
                return
        self._w = d[-1] - self._weight
