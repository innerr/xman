import os
import sys
import time

import punch
import move
import rotate
import shuttle
import trend

class Capture:
    def __init__(self, e, buf = 1024):
        self._e = e
        self._cp = punch.Punch()
        self._cm = move.Move()
        self._cr = rotate.Rotate()
        self._cs = shuttle.Shuttle()
        self._ct1 = trend.Trend()
        self._ct2 = trend.Trend()

        self._max = buf
        self._x = []
        self._y = []
        self._z = []
        self._s = []
        self._d = []

        self._i = long(0)

    def _trim(self):
        d = len(self._s) - self._max
        if d <= 0:
            return
        self._x = self._x[d:]
        self._y = self._y[d:]
        self._z = self._z[d:]
        self._s = self._s[d:]
        self._d = self._d[d:]

    def on(self, a):
        i, self._i = self._i, self._i + 1

        s = a[0] * a[0] + a[1] * a[1] + a[2] * a[2] - 256
        d = (len(self._s) != 0) and (s - self._s[-1]) or 0

        self._x.append(a[0])
        self._y.append(a[1])
        self._z.append(a[2])
        self._s.append(s)
        self._d.append(d)

        self._e.on('tick', a, s, d)

        if len(self._s) < 16:
            return
        self._trim()

        pv = self._cp.on(i, self._s, self._d)
        mv = self._cm.on(i, self._s, self._d)
        rv = self._cr.on(i, self._s, self._d)
        sv = self._cs.on(i, self._s, self._d)
        tv1 = self._ct1.on(i, self._s, self._d)
        tv2 = self._ct2.on(i, self._s, self._d)

        #if mv:
        #    self._e.on('move', mv)
        #if tv1:
        #    self._e.on('move', tv1)
        #if tv2:
        #    self._e.on('trend', tv2)
        if pv:
            self._e.on('punch', pv)

