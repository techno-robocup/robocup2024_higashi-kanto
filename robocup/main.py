#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

DEBUGPRINT = False
DEBUG_MOTOR = False
DEBUG_COLORSENSOR = False

DEFAULT_SPEED = 140
DEFAULT_PROPORTION = 1.1
DEFAULT_I = 0.00055
DEFAULT_D = 15
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

MOTORARM.run(-100)


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
    if COLORLSUM <= 40:
        return True
    return False


def isblack_R() -> bool:
    global COLORRSUM
    if COLORRSUM <= 40:
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
    if max(COLORLR, COLORLG, COLORLB) - min(COLORLR, COLORLG, COLORLB) <= 10:
        return False
    if 175 <= COLORLHUE <= 185 and not isblack_L() and not iswhite_L():
        return True
    return False


def isgreen_R() -> bool:
    global COLORRR, COLORRG, COLORRB, COLORRHUE, COLORRSUM
    if max(COLORRR, COLORRG, COLORRB) - min(COLORRR, COLORRG, COLORRB) <= 10:
        return False
    if 135 <= COLORRHUE < 145 and not isblack_R() and not iswhite_R():
        return True
    return False


def isred_L() -> bool:
    global COLORLR, COLORLG, COLORLB, COLORLHUE, COLORLSUM
    # print("left red check")
    print(max(COLORLR, COLORLG, COLORLB) - min(COLORLR, COLORLG, COLORLB))
    print(COLORLHUE)
    if max(COLORLR, COLORLG, COLORLB) - min(COLORLR, COLORLG, COLORLB) <= 10:
        return False
    if 330 < COLORLHUE or COLORLHUE < 30:
        return True
    return False


def isred_R() -> bool:
    global COLORRR, COLORRG, COLORRB, COLORRHUE, COLORRSUM
    # print("right red check")
    print(max(COLORRR, COLORRG, COLORRB) - min(COLORRR, COLORRG, COLORRB))
    print(COLORRHUE)
    if max(COLORRR, COLORRG, COLORRB) - min(COLORRR, COLORRG, COLORRB) <= 10:
        return False
    if 330 < COLORRHUE or COLORRHUE < 30:
        return True
    return False


def avoid():
    global TOUCHL, TOUCHR, MOTORL, MOTORR
    LBLACK = RBLACK = False
    MOTORL.run(-200)
    MOTORR.run(-200)
    time.sleep(0.3)
    MOTORL.run(200)
    MOTORR.run(-200)
    time.sleep(1)
    while True:
        getline()
        if TOUCHL.pressed():
            MOTORL.run(200)
            MOTORR.run(-200)
        else:
            MOTORL.run(70)
            MOTORR.run(200)
        if isblack_L():
            LBLACK = True
        if isblack_R():
            RBLACK = True
        if LBLACK and RBLACK:
            break
    while not isblack_R():
        getline()
        MOTORL.run(200)
        MOTORR.run(200)
    MOTORL.run(200)
    MOTORR.run(200)
    time.sleep(0.3)
    getline()
    while not isblack_R():
        getline()
        MOTORL.run(200)
        MOTORR.run(-200)
    while isblack_R():
        getline()
        MOTORL.run(200)
        MOTORR.run(-200)



def uturn():
    global MOTORL, MOTORR
    MOTORL.run(200)
    MOTORR.run(-200)
    time.sleep(0.5)
    while not isblack_R():
        getline()
        MOTORL.run(200)
        MOTORR.run(-200)
    while isblack_R():
        getline()
        MOTORL.run(200)
        MOTORR.run(-200)


if DEBUG_COLORSENSOR:
    while True:
        getline()
        EV3.screen.print("L:", COLORLSUM)
        EV3.screen.print("R:", COLORRSUM)
        EV3.screen.print("LHUE:", COLORLHUE)
        EV3.screen.print("RHUE:", COLORRHUE)
        EV3.screen.print(COLORLR, COLORLG, COLORLB)
        EV3.screen.print(COLORRR, COLORRG, COLORRB)
        time.sleep(1)

cnt = 0

while True:
    cnt += 1
    getline()
    if DEBUGPRINT:
        print(COLORLR, COLORLG, COLORLB)
        print(COLORRR, COLORRG, COLORRB)
        print(COLORLHUE)
        print(COLORRHUE)
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
        time.sleep(0.3)
        cnt = 0
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
        MOTORL.run(-200)
        MOTORR.run(200)
        time.sleep(0.3)
        cnt = 0
    if isgreen_L() and cnt >= 40 and not isgreen_R():
        print("isleft")
        EV3.speaker.beep(frequency=1000)
        MOTORL.brake()
        MOTORR.brake()
        time.sleep(1)
        getline()
        if isgreen_R():
            uturn()
            print("uturning")
            continue
        while not isblack_L() and not iswhite_L():
            getline()
            MOTORL.run(200)
            MOTORR.run(200)
        if isblack_L():
            print("correct")
            while isblack_L():
                getline()
                MOTORL.run(200)
                MOTORR.run(200)
            while not isblack_L():
                getline()
                MOTORL.run(-200)
                MOTORR.run(200)
            while isblack_L():
                getline()
                MOTORL.run(-200)
                MOTORR.run(200)
        else:
            print("wrong")
            cnt = 0
    if isgreen_R() and cnt >= 40 and not isgreen_L():
        print("isright")
        EV3.speaker.beep(frequency=2000)
        MOTORL.brake()
        MOTORR.brake()
        time.sleep(1)
        getline()
        if isgreen_L():
            uturn()
            print("Uturning")
            continue
        while not isblack_R() and not iswhite_R():
            getline()
            MOTORL.run(200)
            MOTORR.run(200)
        if isblack_R():
            print("correct")
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
            print("wrong")
            cnt = 0
    if TOUCHL.pressed() and TOUCHR.pressed():
        EV3.speaker.beep(frequency=1000)
        avoid()
    if isgreen_L() and isgreen_R():
        EV3.speaker.beep(frequency=4000)
        uturn()
    if isred_L() and isred_R():
        break
