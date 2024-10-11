#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
DEBUGPRINT = True
DEBUG_MOTOR = False
DEBUG_COLORSENSOR = False

DEFAULT_SPEED = 120
DEFAULT_PROPORTION = 1
DEFAULT_I = 0.00052
DEFAULT_D = 12
WHITE_THRESHOLD = 100
BLACK_THRESHOLD = 50

EV3 = EV3Brick()
MOTORL = Motor(Port.C)
MOTORR = Motor(Port.D)
MOTORARM = Motor(Port.B)
COLORL = ColorSensor(Port.S1)
COLORR = ColorSensor(Port.S2)
TOUCHL = TouchSensor(Port.S4)
TOUCHR = TouchSensor(Port.S3)

COLORLR = 0
COLORLG = 0
COLORLB = 0
COLORRR = 0
COLORRG = 0
COLORRB = 0
COLORLSUM = 0
COLORRSUM = 0
COLORLSUMBEFORE = 0
COLORRSUMBEFORE = 0
COLORLHUE = 0
COLORRHUE = 0
ISUM = 0
DSUM = 0


def calc_hue(r: int, g: int, b: int) -> int:
    if r == g and g == b:
        return 0
    maxnum = max(r, g, b)
    minnum = min(r, g, b)
    if maxnum == b:
        return 60 * ((r - g) / (maxnum - minnum)) + 240
    if maxnum == r:
        return 60 * ((g - b) / (maxnum - minnum))
    if maxnum == g:
        return 60 * ((b - r) / (maxnum - minnum)) + 120

def getline() -> None:
    global COLORL, COLORR, COLORLR, COLORLG, COLORLB, COLORRR, COLORRG, COLORRB, COLORLSUM, COLORRSUM, COLORLHUE, COLORRHUE
    COLORLSUMBEFORE = COLORLSUM
    COLORRSUMBEFORE = COLORRSUM
    COLORLR, COLORLG, COLORLB = COLORL.rgb()
    COLORRR, COLORRG, COLORRB = COLORR.rgb()
    COLORLSUM = COLORLR + COLORLG + COLORLB
    COLORRSUM = COLORRR + COLORRG + COLORRB
    COLORLHUE = calc_hue(COLORLR, COLORLG, COLORLB)
    COLORRHUE = calc_hue(COLORRR, COLORRG, COLORRB)
    ISUM = COLORLSUM - COLORRSUM
    DSUM = (COLORLSUMBEFORE - COLORRSUMBEFORE) - (COLORLSUM - COLORRSUM)
    return None


def isblack_L() -> bool:
    global COLORLSUM
    if COLORLSUM <= 30:
        return True
    return False


def isblack_R() -> bool:
    global COLORRSUM
    if COLORRSUM <= 30:
        return True
    return False


def iswhite_L() -> bool:
    global COLORLSUM
    if COLORLSUM >= 200:
        return True
    return False


def iswhite_R() -> bool:
    global COLORRSUM
    if COLORRSUM >= 200:
        return True
    return False


def isgreen_L() -> bool:
    global COLORLR, COLORLG, COLORLB, COLORLHUE, COLORLSUM
    if max(COLORLR, COLORLG, COLORLB) == min(COLORLR, COLORLG, COLORLB):
        return False
    if 140 < COLORLHUE < 150 and not isblack_L() and not iswhite_L():
        return True


def isgreen_R() -> bool:
    global COLORRR, COLORRG, COLORRB, COLORRHUE, COLORRSUM
    if max(COLORRR, COLORRG, COLORRB) == min(COLORRR, COLORRG, COLORRB):
        return False
    if 125 < COLORRHUE < 130 and not isblack_R() and not iswhite_R():
        return True


if DEBUG_COLORSENSOR:
    while True:
        getline()
        print("L:", COLORLSUM)
        print("R:", COLORRSUM)
        print("LHUE:", COLORLHUE)
        print("RHUE:", COLORRHUE)
        time.sleep(0.1)


cnt = 0

while True:
    cnt+=1
    getline()
    if DEBUGPRINT:
        print("L:", COLORLSUM)
        print("R:", COLORRSUM)
        print("LHUE:", COLORLHUE)
        print("RHUE:", COLORRHUE)
    MOTORL.run(DEFAULT_SPEED + DEFAULT_PROPORTION * (COLORLSUM - COLORRSUM) +
               ISUM * DEFAULT_I + DSUM * DEFAULT_D)
    MOTORR.run(DEFAULT_SPEED + DEFAULT_PROPORTION * (COLORRSUM - COLORLSUM) -
               ISUM * DEFAULT_I - DSUM * DEFAULT_D)
    if isblack_L() and cnt >= 20 and not isblack_R():
        EV3.speaker.beep()
        while isblack_L():
            getline()
            MOTORL.run(200)
            MOTORR.run(200)
        while not isblack_R():
            getline()
            MOTORL.run(-200)
            MOTORR.run(200)
        MOTORL.run(200)
        MOTORR.run(-200)
        cnt=0
    if isblack_R() and cnt >= 20 and not isblack_L():
        EV3.speaker.beep(frequency=1000)
        while isblack_R():
            getline()
            MOTORL.run(200)
            MOTORR.run(200)
        while not isblack_L():
            getline()
            MOTORL.run(200)
            MOTORR.run(-200)
        cnt=0
    if isgreen_L() and cnt >= 20 and not isgreen_R():
        EV3.speaker.beep(frequency=1000)
        MOTORL.brake()
        MOTORR.brake()
        getline()
        if not isgreen_L():
            continue
        while not isblack_L() and not iswhite_L():
            getline()
            MOTORL.run(200)
            MOTORR.run(200)
        if isblack_L():
            while isblack_L():
                getline()
                MOTORL.run(200)
                MOTORR.run(200)
            while not isblack_L():
                getline()
                MOTORL.run(200)
                MOTORR.run(-200)
            while isblack_L():
                getline()
                MOTORL.run(200)
                MOTORR.run(-200)
        else:
            cnt=0
    if isgreen_R() and cnt >= 20 and not isgreen_L():
        EV3.speaker.beep(frequency=2000)
        MOTORL.brake()
        MOTORR.brake()
        getline()
        if not isgreen_R():
            continue
        while not isblack_R() and not iswhite_R():
            getline()
            MOTORL.run(200)
            MOTORR.run(200)
        if isblack_R():
            while isblack_R():
                getline()
                MOTORL.run(200)
                MOTORR.run(200)
            while not isblack_R():
                getline()
                MOTORL.run(200)
                MOTORR.run(-200)
            while isblack_R():
                getline()
                MOTORL.run(200)
                MOTORR.run(-200)
        else:
            cnt=0
