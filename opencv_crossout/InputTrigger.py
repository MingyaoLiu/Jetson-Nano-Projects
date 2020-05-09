# CODE CITATION:
# Inspired from this post
# https://stackoverflow.com/questions/11906925/python-simulate-keydown

import ctypes
import time
import win32api
import win32con

from ctypes import windll

def char2key(c):
    result = windll.User32.VkKeyScanW(ord(str(c)))
    shift_state = (result & 0xFF00) >> 8
    vk_key = result & 0xFF

    return vk_key

# Actuals Functions

def keyPress(*args):
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(char2key(i), 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(char2key(i), 0, win32con.KEYEVENTF_KEYUP, 0)


def keyHold(*args):
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(char2key(i), 0,0,0)
    
def keyRelease(*args):
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(char2key(i), 0, win32con.KEYEVENTF_KEYUP, 0)
    


def mouseClick(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1], 0, 0)

def setMousePos(pos):
    win32api.SetCursorPos(pos)

def getMousePos():
    return win32api.GetCursorPos()
