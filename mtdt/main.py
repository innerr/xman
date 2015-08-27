import os
import sys
from mtdt import game

def handle():
    m = game.Game('wav')
    while True:
        d = sys.stdin.readline()
        if len(d) == 0:
            break
        v = d.split('value: ')
        if len(v) != 2:
            continue
        xyz = v[1][:-1].split(' ')[:3]
        m.recv(xyz)

def run():
    try:
        handle()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    run()

