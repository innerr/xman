class Combo:
    def __init__(self, e, step = 100):
        self._s = 0
        self._c = 0

        def fade(*m):
            self._s -= 4
            self._s = self._s > 0 and self._s or 0
            if self._c > 0 and (self._c - self._s >= step):
                c, self._c = self._c, 0
                self._s = 0
                e.on('combo-', int(c / 100))

        e.register('tick', fade)

        def increase(v):
            self._s += v
            if self._s - self._c >= step:
                self._c = self._s
                e.on('combo+', int(self._c / 100))

        e.register('punch', lambda w: increase(int(w / 2)))
