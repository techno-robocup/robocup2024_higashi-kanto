#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,InfraredSensor, UltrasonicSensor, GyroSensor)
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
__DEBUG__ = False # Turn it on if you want to print debug info into console
__DEBUG__MOTOR__ = False # Turn on if you want to check how the motor is working
__DEBUG__COLORSENSOR__ = False # Turn on if you want to print the colorsensor's data in to console
__DEBUG__COLORSENSOR__GREEN__ = False # Turn on if you want to check whether it is judged as green.
__CONST__CLOCK__ = 1 # Define the clock speed
__CONST__SPEED__ = 70 # The default speed to move
__CONST__WHITE__ = 100
__CONST__BLACK__ = 50
__CONST__PROPORTION__ = 1.3
__CONST__I__ = 0.00052
__CONST__D__ = 12
ev3 = EV3Brick() #<!-- DO NOT CHANGE THE VARIABLE'S NAME --!>
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
_COLORSENSOR_LR_AVG = 0
_COLORSENSOR_L_AVGSUM = 0
_COLORSENSOR_R_AVGSUM = 0
_COLORSENSOR_L_HSV = 0
_COLORSENSOR_R_HSV = 0
_I_SUM = 0
_D_SUM = 0
# Write your program under here.
def getline():
    global __DEBUG__, __DEBUG__MOTOR__, __DEBUG__COLORSENSOR__, __CONST__CLOCK__, __CONST__SPEED__, __CONST__WHITE__, ev3, __CONST__MOTOR__L__, __CONST__MOTOR__R__, __CONST__MOTOR__ARM__, __CONST__COLORSENSOR__L__, __CONST__COLORSENSOR__R__, _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B, _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B, _COLORSENSOR_L_SUM,_COLORSENSOR_R_SUM, __CONST__PROPORTION__, _COLORSENSOR_L_AVGSUM, _COLORSENSOR_R_AVGSUM, _D_SUM, __CONST__D__, _I_SUM, __CONST__D__, _COLORSENSOR_L_SUM_BEFORE, _COLORSENSOR_R_SUM_BEFORE, _COLORSENSOR_L_HSV, _COLORSENSOR_R_HSV
    _COLORSENSOR_L_SUM_BEFORE = _COLORSENSOR_L_SUM
    _COLORSENSOR_R_SUM_BEFORE = _COLORSENSOR_R_SUM
    _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B = __CONST__COLORSENSOR__L__.rgb()
    _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B = __CONST__COLORSENSOR__R__.rgb()
    _COLORSENSOR_L_SUM = _COLORSENSOR_L_R + _COLORSENSOR_L_G + _COLORSENSOR_L_B - 10
    _COLORSENSOR_R_SUM = _COLORSENSOR_R_R + _COLORSENSOR_R_G + _COLORSENSOR_R_B
    _COLORSENSOR_LR_AVG = (_COLORSENSOR_L_SUM + _COLORSENSOR_R_SUM) // 2
    _COLORSENSOR_L_AVGSUM = ((_COLORSENSOR_L_AVGSUM) * (__CONST__CLOCK__ - 1) + _COLORSENSOR_L_SUM) // __CONST__CLOCK__
    _COLORSENSOR_R_AVGSUM = ((_COLORSENSOR_R_AVGSUM) * (__CONST__CLOCK__ - 1) + _COLORSENSOR_R_SUM) // __CONST__CLOCK__
    _I_SUM += _COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM
    _D_SUM = (_COLORSENSOR_L_SUM_BEFORE - _COLORSENSOR_R_SUM_BEFORE) - (_COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM)
def isgreen_L(r,g,b)->bool:
    global _COLORSENSOR_L_HSV
    if(max(r,g,b) == r and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_L_HSV = 60 * (g - b) / (max(r,g,b) - min(r,g,b))
        if(_COLORSENSOR_L_HSV < 0):
            _COLORSENSOR_L_HSV += 360
        if(140 < _COLORSENSOR_L_HSV < 150 and 16 > max(r,g,b) / 255 * 100 > 10 and 31 <= _COLORSENSOR_L_G < 50):
            return True
        return False
    if(max(r,g,b) == g and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_L_HSV = 60 * (b - r) / (max(r,g,b) - min(r,g,b)) + 120
        if(_COLORSENSOR_L_HSV < 0):
            _COLORSENSOR_L_HSV += 360
        if(140 < _COLORSENSOR_L_HSV < 150 and 16 > max(r,g,b) / 255 * 100 > 10 and 31 <= _COLORSENSOR_L_G < 50):
            return True
        return False
    if(max(r,g,b) == b and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_L_HSV = 60 * (r - g) / (max(r,g,b) - min(r,g,b)) + 240
        if(_COLORSENSOR_L_HSV < 0):
            _COLORSENSOR_L_HSV += 360
        if(140 < _COLORSENSOR_L_HSV < 150 and 16 > max(r,g,b) / 255 * 100 > 10 and 31 <= _COLORSENSOR_L_G < 50):
            return True
        return False
    return False
def isgreen_R(r,g,b)->bool:
    global _COLORSENSOR_R_HSV
    if(max(r,g,b) == r and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_R_HSV = 60 * (g - b) / (max(r,g,b) - min(r,g,b))
        if(_COLORSENSOR_R_HSV < 0):
            _COLORSENSOR_R_HSV += 360
        if(127 < _COLORSENSOR_R_HSV < 132 and 17 > max(r,g,b) / 255 * 100 > 13 and 39 <= _COLORSENSOR_R_G <= 43):
            return True
        return False
    if(max(r,g,b) == g and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_R_HSV = 60 * (b - r) / (max(r,g,b) - min(r,g,b)) + 120
        if(_COLORSENSOR_R_HSV < 0):
            _COLORSENSOR_R_HSV += 360
        if(127 < _COLORSENSOR_R_HSV < 132 and 17 > max(r,g,b) / 255 * 100 > 13 and 39 <= _COLORSENSOR_R_G <= 43):
            return True
        return False
    if(max(r,g,b) == b and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_R_HSV = 60 * (r - g) / (max(r,g,b) - min(r,g,b)) + 240
        if(_COLORSENSOR_R_HSV < 0):
            _COLORSENSOR_R_HSV += 360
        if(128 < _COLORSENSOR_R_HSV < 131 and 17 > max(r,g,b) / 255 * 100 > 14 and 39 <= _COLORSENSOR_R_G <= 43):
            return True
        return False
    return False
def isred_R(r,g,b)->bool:
    if 49 >= r >= 38 and 20 >= g and 20 >= b:
        return True
    return False
def isred_L(r,g,b)->bool:
    if 75 >= r >= 56 and 20 >= g and 20 >= b:
        return True
    return False
ev3.speaker.beep()
for _ in range(__CONST__CLOCK__):
    getline()
if __DEBUG__MOTOR__:
    while True:
        for i in range(1000):
            __CONST__MOTOR__L__.run(1000)
            __CONST__MOTOR__R__.run(1000)
        for i in range(1000):
            __CONST__MOTOR__L__.run(-1000)
            __CONST__MOTOR__R__.run(-1000)
if __DEBUG__COLORSENSOR__:
    while True:
        getline()
        print("L: ",_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B)
        print("R: ",_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B)
        time.sleep(1)
for i in range(1000):
   __CONST__MOTOR__ARM__.run(-200)
right_ungle = 0 # 0 means left side is right ungle.
while True:
    if __DEBUG__:
        print("D: ",_D_SUM)
    getline()
    if(not(__DEBUG__COLORSENSOR__GREEN__)):
        __CONST__MOTOR__L__.run(__CONST__SPEED__ * (50 - abs(_D_SUM)) / 40 + __CONST__PROPORTION__*(_COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM) + _I_SUM * __CONST__I__ + _D_SUM * __CONST__D__)
        __CONST__MOTOR__R__.run(__CONST__SPEED__ * (50 - abs(_D_SUM)) / 40 + __CONST__PROPORTION__*(_COLORSENSOR_R_SUM - _COLORSENSOR_L_SUM) - _I_SUM * __CONST__I__ - _D_SUM * __CONST__D__)
    if __DEBUG__COLORSENSOR__GREEN__:
        print(_COLORSENSOR_L_HSV,_COLORSENSOR_L_G,_COLORSENSOR_R_HSV,_COLORSENSOR_R_G,max(_COLORSENSOR_L_B,_COLORSENSOR_L_G,_COLORSENSOR_L_R) / 255 * 100,max(_COLORSENSOR_R_B,_COLORSENSOR_R_G,_COLORSENSOR_R_R) / 255 * 100)
        if isgreen_L(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B):
            print("LEFT GREEN")
            ev3.speaker.beep()
        if isgreen_R(_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B):
            print("RIGHT GREEN")
            ev3.speaker.beep()
    if isgreen_L(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B) and isgreen_R(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B):
        ev3.speaker.beep(frequency=440)
        __CONST__MOTOR__R__.brake()
        __CONST__MOTOR__L__.brake()
        __CONST__MOTOR__L__.run(-100)
        __CONST__MOTOR__R__.run(-100)
        time.sleep(0.7)
        getline()
        __CONST__MOTOR__L__.run(100)
        __CONST__MOTOR__R__.run(-100)
        time.sleep(6.3)
    if isgreen_R(_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B):
        if __DEBUG__COLORSENSOR__GREEN__:
            print("RIGHT GREEN")
        ev3.speaker.beep()
        time.sleep(0.5)
        if(not(__DEBUG__COLORSENSOR__GREEN__)):
            while(_COLORSENSOR_R_G <= 80):
                __CONST__MOTOR__L__.run(80)
                __CONST__MOTOR__R__.run(80)
                getline()
            __CONST__MOTOR__L__.run(80)
            __CONST__MOTOR__R__.run(80)
            time.sleep(0.5)
            while(_COLORSENSOR_R_G >= 20):
                __CONST__MOTOR__L__.run(80)
                __CONST__MOTOR__R__.run(-60)
                getline()
            while(_COLORSENSOR_R_G <= 90):
                __CONST__MOTOR__L__.run(80)
                __CONST__MOTOR__R__.run(-60)
                getline()
            __CONST__MOTOR__L__.run(80)
            __CONST__MOTOR__R__.run(-60)
            time.sleep(0.4)    
    if isgreen_L(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B):
        if __DEBUG__COLORSENSOR__GREEN__:
            print("LEFT GREEN")
        ev3.speaker.beep()
        time.sleep(0.5)
        if(not(__DEBUG__COLORSENSOR__GREEN__)):
            while(_COLORSENSOR_L_G <= 80):
                __CONST__MOTOR__L__.run(80)
                __CONST__MOTOR__R__.run(80)
                getline()
            __CONST__MOTOR__L__.run(80)
            __CONST__MOTOR__R__.run(80)
            time.sleep(0.5)
            while(_COLORSENSOR_L_G >= 20):
                __CONST__MOTOR__L__.run(-80)
                __CONST__MOTOR__R__.run(60)
                getline()
            while(_COLORSENSOR_L_G <= 90):
                __CONST__MOTOR__L__.run(-80)
                __CONST__MOTOR__R__.run(60)
                getline()
            __CONST__MOTOR__L__.run(-80)
            __CONST__MOTOR__R__.run(60)
            time.sleep(0.4)
    """
    if(abs(_D_SUM) > 15):
        __CONST__MOTOR__L__.run(80)
        __CONST__MOTOR__R__.run(80)
        time.sleep(0.7)
        if(0 <= _D_SUM):
            right_ungle = 0
        else:
            right_ungle = 1
        __CONST__MOTOR__L__.run(80)
        __CONST__MOTOR__R__.run(80)
        time.sleep(0.7)
        if(isgreen_L(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B) or isgreen_R(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B)):
            __CONST__MOTOR__L__.run(80)
            __CONST__MOTOR__R__.run(80)
            time.sleep(2)
        elif(right_ungle == 0):
            while(_COLORSENSOR_L_G >= 20):
                __CONST__MOTOR__L__.run(-80)
                __CONST__MOTOR__R__.run(-80)
                getline()
            while(_COLORSENSOR_L_G >= 20):
                __CONST__MOTOR__L__.run(-80)
                __CONST__MOTOR__R__.run(60)
                getline()
            while(_COLORSENSOR_L_G <= 90):
                __CONST__MOTOR__L__.run(-80)
                __CONST__MOTOR__R__.run(60)
                getline()
            __CONST__MOTOR__L__.run(-80)
            __CONST__MOTOR__R__.run(60)
            time.sleep(0.4)
        else:
            while(_COLORSENSOR_L_G >= 20):
                __CONST__MOTOR__L__.run(-80)
                __CONST__MOTOR__R__.run(-80)
                getline()
            while(_COLORSENSOR_L_G >= 20):
                __CONST__MOTOR__L__.run(80)
                __CONST__MOTOR__R__.run(-60)
                getline()
            while(_COLORSENSOR_L_G <= 90):
                __CONST__MOTOR__L__.run(80)
                __CONST__MOTOR__R__.run(-60)
                getline()
            __CONST__MOTOR__L__.run(80)
            __CONST__MOTOR__R__.run(-60)
            time.sleep(0.4)
    """
    if isred_L(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B) and isred_R(_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B):
        ev3.speaker.beep(frequency=550)
        if __DEBUG__:
            print("RED")
        __CONST__MOTOR__L__.run(0)
        __CONST__MOTOR__R__.run(0)
        time.sleep(3)
        __CONST__MOTOR__L__.run(100)
        __CONST__MOTOR__R__.run(100)
        time.sleep(1)