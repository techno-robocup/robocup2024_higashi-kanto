#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
__DEBUG__ = True #デバッグするときにTrueにする
#Trueにするとコンソールへ出力してくれる
#MSVCで言う #ifdef _DEBUG
#のようなもの
__CONST__CLOCK = 15 #プログラムの周期を設定
ev3 = EV3Brick() #ev3オブジェクトの生成
_MOTOR_L = Motor(Port.A) #左モーターオブジェクトの生成
_MOTOR_R = Motor(Port.D) #右モーターオブジェクトの生成
_MOTOR_ARM = Motor(Port.B) #アームモーターオブジェクトの生成
_COLORSENSOR_L = ColorSensor(Port.S1) #左カラーセンサーオブジェクトの生成
_COLORSENSOR_R = ColorSensor(Port.S4) #右カラーセンサーオブジェクトの生成
_COLORSENSOR_L_R = 0 #左カラーセンサーREDの値保存用の変数
_COLORSENSOR_L_G = 0 #GREEN
_COLORSENSOR_L_B = 0 #BLUE
_COLORSENSOR_R_R = 0 #右カラーセンサーREDの値保存用の変数
_COLORSENSOR_R_G = 0 #GREEN
_COLORSENSOR_R_B = 0 #BLUE
_COLORSENSOR_L_AVG = 0 #左カラーセンサーの過去(__CONST__CLOCK)のRGBの合計の平均
_COLORSENSOR_R_AVG = 0 #右カラーセンサーの過去(__CONST__CLOCK)のRGBの合計の平均

# Write your program here.
def getline():
    _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B = _COLORSENSOR_L.rgb() #左カラーセンサーの変数に値を格納
    _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B = _COLORSENSOR_R.rgb() #右カラーセンサーの変数に値を格納
    _COLORSENSOR_L_AVG = (_COLORSENSOR_L_AVG * (__CONST__CLOCK - 1) + _COLORSENSOR_L_R + _COLORSENSOR_L_G + _COLORSENSOR_L_B) // __CONST__CLOCK #左カラーセンサー平均を計算
    _COLORSENSOR_R_AVG = (_COLORSENSOR_R_AVG * (__CONST__CLOCK - 1) + _COLORSENSOR_R_R + _COLORSENSOR_R_G + _COLORSENSOR_R_B) // __CONST__CLOCK #右カラーセンサーの平均を計算
ev3.speaker.beep()
while True:
    for i in range(__CONST__CLOCK): #クロック数回繰り返す
        getline() #変数をリセット
