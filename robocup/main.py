#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
__DEBUG__ = True #デバッグするときにTrueにする
#Trueにするとコンソールへ出力してくれる(ようなプログラムにする)
__DEBUG__MOTOR__ = False #モーターの動作を確認したい時にTrueにする
#モーターが全速力で動く(ようなプログラムを作る)
__DEBUG__COLORSENSOR__ = False #カラーセンサーをデバックするときはTrueに
#カラーセンサーの値をコンソールに出力する(プログラムにする)
__CONST__CLOCK = 3 #プログラムの周期を設定
__CONST__SPEED = 130 #何もなくても100のスピードで動くようにする
__CONST__WHITE = 100 #白として判定する明るさのしきい値
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
    global __CONST__CLOCK, ev3, _MOTOR_L, _MOTOR_R, _MOTOR_ARM, _COLORSENSOR_L, _COLORSENSOR_R, _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B, _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B, _COLORSENSOR_L_AVG, _COLORSENSOR_R_AVG #オブジェクトがグローバル変数であることを明記する
    _COLORSENSOR_L_R, _COLORSENSOR_L_G, _COLORSENSOR_L_B = _COLORSENSOR_L.rgb() #左カラーセンサーの変数に値を格納
    _COLORSENSOR_R_R, _COLORSENSOR_R_G, _COLORSENSOR_R_B = _COLORSENSOR_R.rgb() #右カラーセンサーの変数に値を格納
    _COLORSENSOR_L_AVG = (_COLORSENSOR_L_AVG * (__CONST__CLOCK - 1) + _COLORSENSOR_L_R + _COLORSENSOR_L_G + _COLORSENSOR_L_B) // __CONST__CLOCK #左カラーセンサー平均を計算
    _COLORSENSOR_R_AVG = (_COLORSENSOR_R_AVG * (__CONST__CLOCK - 1) + _COLORSENSOR_R_R + _COLORSENSOR_R_G + _COLORSENSOR_R_B) // __CONST__CLOCK #右カラーセンサーの平均を計算
ev3.speaker.beep()
if __DEBUG__MOTOR__: #もしモーターでバッグが定義されていたら
    while True:
        _MOTOR_L.run(150) #右モーターを動かす
        _MOTOR_R.run(150) #左モーターを動かす
if __DEBUG__COLORSENSOR__: #カラーセンサーデバックが定義されていたら
    while True: #ずっと
        getline()
        print(_COLORSENSOR_L_AVG, _COLORSENSOR_R_AVG) #平均を出力
for _ in range(__CONST__CLOCK):
    getline()
while True:
    getline()
    if __DEBUG__:
        print(_COLORSENSOR_L_AVG, _COLORSENSOR_R_AVG) #平均を出力する
    _MOTOR_L.run((_COLORSENSOR_L_AVG - _COLORSENSOR_R_AVG) * 3 + __CONST__SPEED)
    _MOTOR_R.run((_COLORSENSOR_R_AVG - _COLORSENSOR_L_AVG) * 3 + __CONST__SPEED)
    if _COLORSENSOR_L_AVG < __CONST__WHITE: #もししばらく暗くなったら
        if __DEBUG__:
            print("LEFT BLACK", _COLORSENSOR_L_AVG, _COLORSENSOR_R_AVG)
        while _COLORSENSOR_L_AVG < __CONST__WHITE: #暗い間
            if __DEBUG__:
                print("going straight")
            getline() #センサーの値を更新して
            _MOTOR_L.run(__CONST__SPEED) #左モーターを進める
            _MOTOR_R.run(__CONST__SPEED) #右モーターを進める
        while _COLORSENSOR_L_AVG > __CONST__WHITE: #明るい間
            print("now white")
            getline()
            _MOTOR_L.run(70) #左に
            _MOTOR_R.run(150) #回転する
        _COLORSENSOR_L_AVG = __CONST__WHITE - 1 #少し数値を補正
        #次のwhile文に引っかからないといけないため
        while _COLORSENSOR_L_AVG < __CONST__WHITE: #暗い間
            print("now black")
            getline()
            _MOTOR_L.run(70) #左に
            _MOTOR_R.run(150) #回転する
        if __DEBUG__:
            print("LEFT END", _COLORSENSOR_L_AVG, _COLORSENSOR_R_AVG)
