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
__DEBUG__ = False # Turn it on if you want to print debug info into console
__DEBUG__MOTOR__ = False # Turn on if you want to check how the motor is working
__DEBUG__COLORSENSOR__ =False # Turn on if you want to print the colorsensor's data in to console
__DEBUG__COLORSENSOR__GREEN__ = False # Turn on if you want to check whether it is judged as green.
__CONST__CLOCK__ = 1 # Define the clock speed
__CONST__SPEED__ = 120 # The default speed to move
__CONST__WHITE__ = 100 # The threshold for recognizing as WHITE
__CONST__BLACK__ = 50 # The threshold for recognizing as BLACK
__CONST__PROPORTION__ = 2.25
__CONST__I__ = 0.00058
__CONST__D__ = 12
ev3 = EV3Brick() #<!-- DO NOT CHANGE THE VARIABLE'S NAME --!>
__CONST__MOTOR__L__ = Motor(Port.A)
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
# Write your program here.
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
"""
def avoid():
    global __DEBUG__, __DEBUG__MOTOR__, __DEBUG__COLORSENSOR__, __CONST__CLOCK__, __CONST__SPEED__, __CONST__WHITE__, ev3, __CONST__MOTOR__L__, __CONST__MOTOR__R__, __CONST__MOTOR__ARM__, __CONST__COLORSENSOR__L__, __CONST__COLORSENSOR__R__, _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B, _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B, _COLORSENSOR_L_SUM,_COLORSENSOR_R_SUM, __CONST__PROPORTION__, _COLORSENSOR_L_AVGSUM, _COLORSENSOR_R_AVGSUM, _COLORSENSOR_L_HSV, _COLORSENSOR_R_HSV
    for i in range(2000):
        __CONST__MOTOR__L__.run(-2000)
        __CONST__MOTOR__R__.run(2000)
    for i in range(3000):
        __CONST__MOTOR__L__.run(-1000)
        __CONST__MOTOR__R__.run(2000)
    while(_COLORSENSOR_L_SUM < 50 or _COLORSENSOR_R_SUM < 50):
        __CONST__MOTOR__L__.run(-1000)
        __CONST__MOTOR__R__.run(2000)
        if(__CONST__TOUCHSENSOR_R.pressed()):
            __CONST__MOTOR__L__.run(-2000)
            __CONST__MOTOR__R__.run(1000)
"""
def isgreen_L(r,g,b)->bool:
    global _COLORSENSOR_L_HSV

    if(max(r,g,b) == r and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_L_HSV = 60 * (g - b) / (max(r,g,b) - min(r,g,b))
        if(_COLORSENSOR_L_HSV < 0):
            _COLORSENSOR_L_HSV += 360
        if(140 < _COLORSENSOR_L_HSV < 170 and 20 > max(r,g,b) / 255 * 100 > 10):
            return True
        return False
    if(max(r,g,b) == g and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_L_HSV = 60 * (b - r) / (max(r,g,b) - min(r,g,b)) + 120
        if(_COLORSENSOR_L_HSV < 0):
            _COLORSENSOR_L_HSV += 360
        if(140 < _COLORSENSOR_L_HSV < 170 and 20 > max(r,g,b) / 255 * 100 > 10):
            return True
        return False
    if(max(r,g,b) == b and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_L_HSV = 60 * (r - g) / (max(r,g,b) - min(r,g,b)) + 240
        if(_COLORSENSOR_L_HSV < 0):
            _COLORSENSOR_L_HSV += 360
        if(140 < _COLORSENSOR_L_HSV < 170 and 20 > max(r,g,b) / 255 * 100 > 10):
            return True
        return False
    return False
def isgreen_R(r,g,b)->bool:
    global _COLORSENSOR_R_HSV
    if(max(r,g,b) == r and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_R_HSV = 60 * (g - b) / (max(r,g,b) - min(r,g,b))
        if(_COLORSENSOR_R_HSV < 0):
            _COLORSENSOR_R_HSV += 360
        if(135 < _COLORSENSOR_R_HSV < 155 and 20 > max(r,g,b) / 255 * 100 > 10):
            return True
        return False
    if(max(r,g,b) == g and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_R_HSV = 60 * (b - r) / (max(r,g,b) - min(r,g,b)) + 120
        if(_COLORSENSOR_R_HSV < 0):
            _COLORSENSOR_R_HSV += 360
        if(135 < _COLORSENSOR_R_HSV < 155 and 20 > max(r,g,b) / 255 * 100 > 10):
            return True
        return False
    if(max(r,g,b) == b and max(r,g,b) - min(r,g,b) != 0):
        _COLORSENSOR_R_HSV = 60 * (r - g) / (max(r,g,b) - min(r,g,b)) + 240
        if(_COLORSENSOR_R_HSV < 0):
            _COLORSENSOR_R_HSV += 360
        if(135 < _COLORSENSOR_R_HSV < 155 and 20 > max(r,g,b) / 255 * 100 > 10):
            return True
        return False
    return False
ev3.speaker.beep()
for _ in range(__CONST__CLOCK__):
    getline()
# <!-- DEBUG MOTOR -->
if __DEBUG__MOTOR__:
    while True:
        for i in range(1000):
            __CONST__MOTOR__L__.run(1000)
            __CONST__MOTOR__R__.run(1000)
        for i in range(1000):
            __CONST__MOTOR__L__.run(-1000)
            __CONST__MOTOR__R__.run(-1000)
# <!-- DEBUG COLORSENSOR -->
if __DEBUG__COLORSENSOR__:
    while True:
        getline()
        print(_COLORSENSOR_L_SUM,_COLORSENSOR_R_SUM)
        print(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B)
        print(_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B)
        time.sleep(1)
for i in range(1000):
    __CONST__MOTOR__ARM__.run(-1000)
while True:
    if __DEBUG__:
        print(__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_R_AVGSUM - _COLORSENSOR_L_AVGSUM),__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_L_AVGSUM - _COLORSENSOR_R_AVGSUM))
        print(__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM) + _I_SUM * __CONST__I__ + _D_SUM * __CONST__D__,__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_R_SUM - _COLORSENSOR_L_SUM) - _I_SUM * __CONST__I__ - _D_SUM * __CONST__D__)
        print(_COLORSENSOR_L_SUM,_COLORSENSOR_R_SUM)
        print(_I_SUM * __CONST__I__)
        print(_D_SUM * __CONST__D__)
    getline()
    __CONST__MOTOR__L__.run(__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM) + _I_SUM * __CONST__I__ + _D_SUM * __CONST__D__)
    __CONST__MOTOR__R__.run(__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_R_SUM - _COLORSENSOR_L_SUM) - _I_SUM * __CONST__I__ - _D_SUM * __CONST__D__)
    if __DEBUG__COLORSENSOR__GREEN__:
        print(_COLORSENSOR_L_HSV,_COLORSENSOR_R_HSV,max(_COLORSENSOR_L_B,_COLORSENSOR_L_G,_COLORSENSOR_L_R) / 255 * 100,max(_COLORSENSOR_R_B,_COLORSENSOR_R_G,_COLORSENSOR_R_R) / 255 * 100)
    if isgreen_R(_COLORSENSOR_R_R,_COLORSENSOR_R_G,_COLORSENSOR_R_B):
        if __DEBUG__COLORSENSOR__GREEN__:
            print("RIGHT GREEN")
        ev3.speaker.beep()
        time.sleep(0.5)
        ev3.speaker.beep()
        start=time.time()
        """
        while time.time()-start<=0.8:
            __CONST__MOTOR__L__.run(150)
            __CONST__MOTOR__R__.run(150)
        ev3.speaker.beep()
        while time.time()-start<=3:
            __CONST__MOTOR__L__.run(150)
            __CONST__MOTOR__R__.run(-200)
        ev3.speaker.beep()
        while time.time()-start<=2:
            __CONST__MOTOR__L__.run(150)
            __CONST__MOTOR__R__.run(180)
        """
    if isgreen_L(_COLORSENSOR_L_R,_COLORSENSOR_L_G,_COLORSENSOR_L_B):
        if __DEBUG__COLORSENSOR__GREEN__:
            print("LEFT GREEN")
        ev3.speaker.beep()
        time.sleep(0.5)
        start=time.time()
        """
        while time.time()-start<=0.8:
            __CONST__MOTOR__L__.run(150)
            __CONST__MOTOR__R__.run(150)
        ev3.speaker.beep()
        while time.time()-start<=3:
            __CONST__MOTOR__L__.run(-200)
            __CONST__MOTOR__R__.run(150)
        ev3.speaker.beep()
        while time.time()-start<=2:
            __CONST__MOTOR__L__.run(180)
            __CONST__MOTOR__R__.run(150)
        """
