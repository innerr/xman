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

