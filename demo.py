# coding: utf-8
__author__ = 'fripSide'

import re
import sys
import subprocess

FROM = "192.168.57.102:5555"
TO = "192.168.57.103:5555"
GETEVENT = "adb -s {} shell getevent -tt"
SENDEVENT = "adb -s {} shell sendevent {}"

EV_NUM = re.compile("")


def play(cmd):
    sc = SENDEVENT.format(TO, cmd)
    print(sc)
    subprocess.check_call([sc], shell=True)

def translate(cmd):
    # print(cmd)
    tokens = cmd.split(" ")
    if tokens[0]  == "[":
        ev = tokens[3][:-1]
        m = " ".join([ev] + [str(int(x, 16)) for x in tokens[4:]])
        play(m)

def record():
    cmd = GETEVENT.format(FROM)
    print(cmd)
    rp = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    # rp.communicate()
    while rp.poll() is None:
        output = rp.stdout.readline()
        # print("raw cmd", output)
        translate(output)


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