#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
# FROM UNDER THIS LINE,
# DO NOT CHANGE THE NAME THAT STARTS FROM '__'
# DO NOT DELETE THE VARIABLE THAT STARTS FROM '_'
# PUT '__CONST__' BEFORE AN CONSTANT VARIABLE
# IF YOU ARE MAKING A TEMPORARY VARIABLE, START THE VARIABLE'S NAME FROM AN small alphabet
__DEBUG__ = False  # Turn it on if you want to print debug info into console
__DEBUG__MOTOR__ = False  # Turn on if you want to check how the motor is working
__DEBUG__COLORSENSOR__ = False  # Turn on if you want to print the colorsensor's data in to console
__DEBUG__COLORSENSOR__GREEN__ = False  # Turn on if you want to check whether it is judged as green.
__CONST__SPEED__ = 70  # The default speed to move
__CONST__WHITE__ = 100
__CONST__BLACK__ = 50
__CONST__PROPORTION__ = 1.3
__CONST__I__ = 0.00052
__CONST__D__ = 12
ev3 = EV3Brick()  # <!-- DO NOT CHANGE THE VARIABLE'S NAME --!>
__CONST__MOTOR__L__ = Motor(Port.C)
__CONST__MOTOR__R__ = Motor(Port.D)
__CONST__MOTOR__ARM__ = Motor(Port.B)
__CONST__COLORSENSOR__L__ = ColorSensor(Port.S1)
__CONST__COLORSENSOR__R__ = ColorSensor(Port.S2)
__CONST__TOUCHSENSOR_L = TouchSensor(Port.S4)
__CONST__TOUCHSENSOR_R = TouchSensor(Port.S3)
_COLORSENSOR_L_R = 0
_COLORSENSOR_L_G = 0
_COLORSENSOR_L_B = 0
_COLORSENSOR_R_R = 0
_COLORSENSOR_R_G = 0
_COLORSENSOR_R_B = 0
_COLORSENSOR_L_SUM = 0
_COLORSENSOR_R_SUM = 0
_COLORSENSOR_L_SUM_BEFORE = 0
_COLORSENSOR_R_SUM_BEFORE = 0
_COLORSENSOR_L_HSV = 0
_COLORSENSOR_R_HSV = 0
_I_SUM = 0
_D_SUM = 0

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

def getline()->None:
    global __CONST__COLORSENSOR__L__,__CONST__COLORSENSOR__R__,_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B,_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B,_COLORSENSOR_L_SUM,_COLORSENSOR_R_SUM,_COLORSENSOR_L_SUM_BEFORE,_COLORSENSOR_R_SUM_BEFORE,_COLORSENSOR_L_HSV,_COLORSENSOR_R_HSV,_I_SUM,_D_SUM
    _COLORSENSOR_L_SUM_BEFORE = _COLORSENSOR_L_SUM
    _COLORSENSOR_R_SUM_BEFORE = _COLORSENSOR_R_SUM
    _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B = __CONST__COLORSENSOR__L__.rgb()
    _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B = __CONST__COLORSENSOR__R__.rgb()
    _COLORSENSOR_L_SUM = _COLORSENSOR_L_R + _COLORSENSOR_L_G + _COLORSENSOR_L_B
    _COLORSENSOR_R_SUM = _COLORSENSOR_R_R + _COLORSENSOR_R_G + _COLORSENSOR_R_B
    _COLORSENSOR_L_HSV = calc_hue(_COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B)
    _COLORSENSOR_R_HSV = calc_hue(_COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B)
    _I_SUM += _COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM
    _D_SUM = (_COLORSENSOR_L_SUM_BEFORE - _COLORSENSOR_R_SUM_BEFORE)-(_COLORSENSOR_L_SUM-_COLORSENSOR_R_SUM)
    return None

def isgreen_L(r:int,g:int,b:int):
    global _COLORSENSOR_L_HSV
    if max(r,g,b)-min(r,g,b)==0:
        return False
    if 140<_COLORSENSOR_L_HSV<150 and 50<=_COLORSENSOR_L_SUM<=200:
        return True

def isgreen_R(r:int,g:int,b:int):
    global _COLORSENSOR_R_HSV
    if max(r,g,b)-min(r,g,b)==0:
        return False
    if 127<_COLORSENSOR_L_HSV<132 and 50<=_COLORSENSOR_L_SUM<=200:
        return True


