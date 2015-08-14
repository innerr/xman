import os
import sys
import time
import math

class CaptureShuttle:
    def __init__(self, e):
        self._e = e

    def on(self, i, v):
        pass

class CaptureMove:
    def __init__(self, e):
        self._e = e

    def on(self, i, v):
        pass

class CapturePunch:
    def __init__(self, e, weight = 300, burstiness = 2):
        self._e = e
        self._weight = weight
        self._burstiness = burstiness
        self._w = 0

    def on(self, i, v):
        if self._w > 0 and v[-1] - v[-2] <= 0:
            self._e.on('punch', int(math.sqrt(int(self._w))))
            self._w = 0
            return
        d = []
        for j in range(0, self._burstiness):
            d.append(v[-1 - j] - v[-2 - j])
        for n in d:
            if 0 < n and n < self._weight:
                return
        self._w = d[0] - self._weight

class CaptureAll:
    def __init__(self, e, buf = 1024):
        self._e = e
        self._cs = CaptureShuttle(e)
        self._ce = CapturePunch(e)
        self._cm = CaptureMove(e)

        self._max = buf
        self._x = []
        self._y = []
        self._z = []
        self._s = []

    def on(self, i, a):
        self._e.on('tick', a)

        s = a[0] * a[0] + a[1] * a[1] + a[2] * a[2] - 256
        self._x.append(a[0])
        self._y.append(a[1])
        self._z.append(a[2])
        self._s.append(s)

        d = len(self._s) - self._max
        if d > 0:
            self._x = self._x[d:]
            self._y = self._y[d:]
            self._z = self._z[d:]
            self._s = self._s[d:]

        if len(self._s) < 16:
            return

        self._e.on('delta', self._s[-1], self._s[-1] - self._s[-2])

        self._cs.on(i, self._s)
        self._ce.on(i, self._s)
        self._cm.on(i, self._s)

class Events:
    def __init__(self):
        self._s = {}

    def register(self, e, f):
        if self._s.has_key(e):
            self._s[e].append(f)
        else:
            self._s[e] = [f]

    def on(self, e, *args):
        if not self._s.has_key(e):
            return
        map(lambda f: f(*args), self._s[e])

class Player:
    def __init__(self, path):
        self._path = path
        self._times = {}
        self._playing = {}

    def register(self, n, t):
        self._times[n] = t
        self._playing[n] = 0

    def play(self, n):
        #if self._playing[n] > time.time():
        #    return
        t = self._times[n]
        #self._playing[n] = time.time() + t
        self._play(n, t)

    def _play(self, n, t):
        os.system('timeout ' + str(t) + ' aplay wav/' + str(n) + '.wav >/dev/null 2>&1 &')

def handle():
    p = Player('wav')
    p.register(6, 2)
    p.register(5, 0.5)
    p.register(4, 1.7)
    p.register(3, 0.5)
    p.register(2, 0.9)
    p.register(1, 0.2)

    def show(m):
        print m

    def tick(a):
        a = map(lambda n: n * 25 / 4, a)
        print '[' + str(time.time()) + ']', a[0], a[1], a[2]

    def shuttle(d):
        print '=>', d
        if d > 10:
            p.play(3)
        elif d > 3:
            p.play(2)

    def punch(w):
        #n = w >= 120 and 6 or (w / 20) or 1
        n = 1
        if w >= 150:
            n = 6
        elif w >= 120:
            n = 5
        elif w >= 60:
            n = 4
        elif w >= 40:
            n = 3
        elif w >= 20:
            n = 2
        elif w >= 0:
            n = 1
        p.play(n)

    e = Events()

    #e.register('tick', tick)
    e.register('delta', lambda s, d: show('#'))
    #e.register('delta', lambda s, d: show(str(s) + ', ' + str(d)))
    #e.register('shuttle', shuttle)
    e.register('punch', lambda w: show('=' * w + '> Punch ' + str(w)))
    e.register('punch', punch)

    c = CaptureAll(e)

    i = long(0)
    while True:
        d = sys.stdin.readline()
        if len(d) == 0:
            break
        v = d.split('value: ')
        if len(v) != 2:
            continue

        a = v[1][:-1].split(' ')[:3]
        a = map(lambda n: int(n, base=16), a)
        a = map(lambda n: n >= 0x80 and (n - 0x100) or n, a)
        c.on(i, a)
        i += 1

def run():
    try:
        handle()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    run()
