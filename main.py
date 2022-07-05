from subprocess import run, PIPE
from time import sleep
import cv2
import numpy as np

port = 54831
_DIR_ANDROID_CAPTURE = "/sdcard/_capture.png"
_DIR_INTERNAL_CAPTURE_FOLDER = "C:/Users/kouta/Desktop/arknights/img"
_DIR_INTERNAL_CAPTURE = "C:/Users/kouta/Desktop/arknights/img/_capture.png"
_DIR_TEMP1 = "./img/temp1.png"
_DIR_TEMP2 = "./img/temp2.png"
_DIR_TEMP3 = "./img/temp3.png"
_DIR_TEMP4 = "./img/temp4.png"
_THRESHOLD = 0.9

def doscmd(directory, command):
    completed_process = run(command, stdout=PIPE, shell=True, cwd=directory, universal_newlines=True, timeout=10)
    return completed_process.stdout

def send_cmd_to_adb(cmd):
    _dir = "C:/Program Files/BlueStacks_nxt"
    return doscmd(_dir, cmd)

def connect_adb(port):
    _cmd = "HD-Adb connect 127.0.0.1:" + str(port)
    send_cmd_to_adb(_cmd)

def tap(x, y):
    _cmd = "HD-Adb shell input touchscreen tap"+ " " + str(x) + " " + str(y)
    send_cmd_to_adb(_cmd)

def show_log():
    _cmd = "HD-Adb logcat -d"
    _pipe = send_cmd_to_adb(_cmd)
    return _pipe

def capture_screen(dir_android, folder_name):
    _cmd = "HD-Adb shell screencap -p" + " " + dir_android
    _pipe = send_cmd_to_adb(_cmd)

    _cmd = "HD-Adb pull" + " " + dir_android + " " + folder_name
    send_cmd_to_adb(_cmd)

def get_center_position_from_tmp(dir_input, dir_tmp):
    _input = cv2.imread(dir_input)
    _temp = cv2.imread(dir_tmp)

    cv2.cvtColor(_input, cv2.COLOR_RGB2GRAY)
    cv2.cvtColor(_temp, cv2.COLOR_RGB2GRAY)

    _h, _w, _none  = _temp.shape

    _match = cv2.matchTemplate(_input, _temp, cv2.TM_CCOEFF_NORMED)
    _loc = np.where(_match >= _THRESHOLD)
    try:
        _x = _loc[1][0]
        _y = _loc[0][0]
        return _x + _w / 2, _y + _h / 2
    except IndexError as e:
        return -1, -1

connect_adb(port)

while True:
    capture_screen(_DIR_ANDROID_CAPTURE, _DIR_INTERNAL_CAPTURE_FOLDER)
    x, y = get_center_position_from_tmp(_DIR_INTERNAL_CAPTURE , _DIR_TEMP4) #スタミナ回復
    tap(x, y)
    x, y = get_center_position_from_tmp(_DIR_INTERNAL_CAPTURE , _DIR_TEMP1) #セレクト1
    tap(x, y)
    x, y = get_center_position_from_tmp(_DIR_INTERNAL_CAPTURE , _DIR_TEMP2) #セレクト2
    tap(x, y)
    x, y = get_center_position_from_tmp(_DIR_INTERNAL_CAPTURE , _DIR_TEMP3) #リザルト
    tap(x, y)
    

