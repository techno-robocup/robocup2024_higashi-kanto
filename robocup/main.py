#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
# Does not have for __DEBUG__ to be True
# FROM UNDER THIS LINE, 
# DO NOT CHANGE THE NAME THAT STARTS FROM '__'
# DO NOT DELETE THE VARIABLE THAT STARTS FROM '_'
# PUT '__CONST__' BEFORE AN CONSTANT VARIABLE
# IF YOU ARE MAKING A TEMPORARY VARIABLE, START THE VARIABLE'S NAME FROM AN small alphabet
__DEBUG__ = True # Turn it on if you want to print debug info into console
__DEBUG__MOTOR__ = True # Turn on if you want to check how the motor is working
__DEBUG__COLORSENSOR__ = False # Turn on if you want to print the colorsensor's data in to console
__CONST__CLOCK__ = 3 # Define the clock speed
__CONST__SPEED__ = 50 # The default speed to move
__CONST__WHITE__ = 100 # The threshold for recognizing as WHITE
__CONST__PROPORTION__ = 3
ev3 = EV3Brick() #<!-- DO NOT CHANGE THE VARIABLE'S NAME --!>
__CONST__MOTOR__L__ = Motor(Port.A)
__CONST__MOTOR__R__ = Motor(Port.D)
__CONST__MOTOR__ARM__ = Motor(Port.B)
__CONST__COLORSENSOR__L__ = ColorSensor(Port.S1)
__CONST__COLORSENSOR__R__ = ColorSensor(Port.S2)
_COLORSENSOR_L_R = 0
_COLORSENSOR_L_G = 0
_COLORSENSOR_L_B = 0
_COLORSENSOR_R_R = 0
_COLORSENSOR_R_G = 0
_COLORSENSOR_R_B = 0
_COLORSENSOR_L_SUM = 0
_COLORSENSOR_R_SUM = 0
# Write your program here.
def getline():
    global __DEBUG__, __DEBUG__MOTOR__, __DEBUG__COLORSENSOR__, __CONST__CLOCK__, __CONST__SPEED__, __CONST__WHITE__, ev3, __CONST__MOTOR__L__, __CONST__MOTOR__R__, __CONST__MOTOR__ARM__, __CONST__COLORSENSOR__L__, __CONST__COLORSENSOR__R__, _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B, _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B, _COLORSENSOR_L_SUM,_COLORSENSOR_R_SUM, __CONST__PROPORTION__
    _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B = __CONST__COLORSENSOR__L__.rgb()
    _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B = __CONST__COLORSENSOR__R__.rgb()
    _COLORSENSOR_L_SUM = _COLORSENSOR_L_R + _COLORSENSOR_L_G + _COLORSENSOR_L_B
    _COLORSENSOR_R_SUM = _COLORSENSOR_R_R + _COLORSENSOR_R_G + _COLORSENSOR_R_B
ev3.speaker.beep()
for i in range(1000):
    __CONST__MOTOR__ARM__.run(-100)
if __DEBUG__MOTOR__:
    while True:
        for i in range(1000):
            __CONST__MOTOR__L__.run(1000)
            __CONST__MOTOR__R__.run(1000)
        for i in range(1000):
            __CONST__MOTOR__L__.run(-1000)
            __CONST__MOTOR__R__.run(-1000)
while True:
    if __DEBUG__:
        print(_COLORSENSOR_L_SUM, _COLORSENSOR_R_SUM)
        print(_COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM, _COLORSENSOR_R_SUM - _COLORSENSOR_L_SUM)
    getline()
    __CONST__MOTOR__L__.run(__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_L_SUM - _COLORSENSOR_R_SUM))
    __CONST__MOTOR__R__.run(__CONST__SPEED__ + __CONST__PROPORTION__*(_COLORSENSOR_R_SUM - _COLORSENSOR_L_SUM))
