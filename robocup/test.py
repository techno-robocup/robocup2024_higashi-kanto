#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

DEBUGPRINT = True
DEBUG_MOTOR = False
DEBUG_COLORSENSOR = False

DEFAULT_SPEED = 90
DEFAULT_PROPORTION = 1.0
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


def calc_hue(r: int, g: int, b: int) -> bool:
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
    COLORRSUM = COLORR + COLORRG + COLORRB
    COLORLHUE = calc_hue(COLORLR, COLORLG, COLORLB)
    COLORRHUE = calc_hue(COLORRR, COLORRG, COLORRB)
    ISUM = COLORLSUM - COLORRSUM
    DSUM = (COLORLSUMBEFORE - COLORRSUMBEFORE) - (COLORLSUM - COLORRSUM)
    return None


def isgreen_L(r: int, g: int, b: int):
    global COLORLHUE, COLORLSUM
    if max(r, g, b) == min(r, g, b):
        return False
    if 140 < COLORLHUE < 150 and 50 <= COLORLSUM <= 200:
        return True


def isgreen_R(r: int, g: int, b: int):
    global COLORRHUE, COLORRSUM
    if max(r, g, b) == min(r, g, b):
        return False
    if 127 < COLORRHUE < 132 and 50 <= COLORRSUM <= 200:
        return True
