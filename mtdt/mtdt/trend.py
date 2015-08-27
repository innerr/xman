class Trend:
    def __init__(self):
        self._i = 0
        self._w = 0

    def on(self, i, v, d):
        m = self._matched(i, v, d)
        if m == None:
            return
        k, w = m
        if w > 0:
            self._w = w
            self._i = i
        else:
            if i - k - self._i > 2:
                return
        return abs(w)

    def _matched(self, i, v, d):
        s = 0
        j = 0
        m = 0
        k = 0
        while j < 16:
            c = s + d[-j - 1]
            if s > 0 and c < 0 or s < 0 and c > 0:
                return
            s = c
            if abs(s) > abs(m):
                m = s
                k = j
            j += 1

        d = d[-k:]
        for n in d:
            if (abs(m) - abs(m - n)) < abs(m / 5):
                m -= n
                k -= 1

        w = int(m / (k + 1))
        #print '*' * 150, k, w
        if k < 2:
            return
        if abs(w) > 400:
            return

        return k, w
