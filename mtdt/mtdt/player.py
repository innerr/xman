import os

class Player:
    def __init__(self, path):
        self._path = path
        self._times = {}

    def register(self, n, t):
        self._times[n] = t

    def play(self, n):
        self._play(n, self._times[n])

    def _play(self, n, t):
        os.system('timeout ' + str(t) + ' aplay wav/' + str(n) + '.wav >/dev/null 2>&1 &')


