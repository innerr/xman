import time
import player
import events
import capture
import combo

class Player:
    def __init__(self, path):
        p = player.Player(path)
        self.play = p.play

        p.register('p1', 0.2)
        p.register('p2', 0.9)
        p.register('p3', 0.5)
        p.register('p4', 1.7)
        p.register('p5', 2)

        p.register('m1', 0.8)
        p.register('m2', 0.9)

        p.register('c1', 9)
        p.register('c2', 9)
        p.register('c3', 9)
        p.register('c4', 9)
        p.register('c5', 9)
        p.register('c6', 9)

class Screen:
    def show(self, m, w):
        print '\033[31;40m=' * w + '> ' + m + ' ' + str(w) + '\033[0m'

    def hl(self, m, w):
        print '\033[31;46m=' * w + '> ' + m + ' ' + str(w) + '\033[0m'

    def track(self, a, s, d):
        d1 = (d > 0) and d or 0
        d2 = (d < 0) and d or 0
        if s < 0:
            d1, d2 = -d2, -d1
        fmt = '[%.2f] % 4d % 4d % 4d  | % 6d % 6d % 6d % 6d'
        print fmt % (time.time(), a[0], a[1], a[2], s, d, d1, d2)

    def xyz(self, a, s, d):
        s1 = a[0]
        s2 = a[1]
        s3 = a[2]
        if not hasattr(self, '_l'):
            self._l = [s1, s2, s3]
        d1 = s1 - self._l[0]
        d2 = s2 - self._l[1]
        d3 = s3 - self._l[2]
        self._l[0] = s1
        self._l[1] = s2
        self._l[2] = s3
        fmt = '[%.2f] % 4d % 4d % 4d  | % 4d % 4d % 4d'
        print fmt % (time.time(), a[0], a[1], a[2], d1, d2, d3)

    def tick(self, a, s, d):
        fmt = '[%.2f] % 4d % 4d % 4d  | % 6d % 6d'
        print fmt % (time.time(), a[0], a[1], a[2], s, d)

class Script:
    def __init__(self, e, path):
        p = Player(path)
        c = Screen()
        b = combo.Combo(e)

        def play(w, v, s):
            for i in range(0, len(v)):
                if w < v[i]:
                    continue
                p.play(s[i])
                return

        def punch(w):
            v = [120, 60, 40, 20, 0]
            s = ['p5', 'p4', 'p3', 'p2', 'p1']
            play(w, v, s)

        def move(w):
            p.play('m1')

        def rotate(w):
            pass

        def shuttle(w):
            pass

        def comboi(w):
            p.play('c' + str(w % 7 or 6))

        e.register('tick', c.track)
        e.register('punch', lambda w: c.show('Punch', w))
        e.register('move', lambda w: c.show('Move', w))
        e.register('rotate', lambda w: c.show('Rotate', w))
        e.register('shuttle', lambda w: c.show('Shuttle', w))
        e.register('combo+', lambda w: c.hl('Combo++', w))
        e.register('combo-', lambda w: c.show('Combo--', w))
        e.register('trend+', lambda w: c.show('Trend++', w))

        e.register('punch', punch)
        e.register('move', move)
        e.register('rotate', rotate)
        e.register('shuttle', shuttle)
        e.register('combo+', comboi)

class Game:
    def __init__(self, path):
        e = events.Events()
        s = Script(e, path)
        self._capture = capture.Capture(e)

    def recv(self, a):
        a = map(lambda n: int(n, base = 16), a)
        a = map(lambda n: n >= 0x80 and (n - 0x100) or n, a)
        self._capture.on(a)

