from sys import platform

import d3dshot

import matplotlib.pyplot as plt
import time
import os
import cv2
import math

import east_recognition

import pytesseract

import random

import InputTrigger

from protobuf_settings import Settings

import numpy as np

import Constants as const

import operator

def getCorrectPos(pos):
    return (int(Settings().settings.shiftX + pos[0]), int(Settings().settings.shiftY + pos[1]))




isAlreadySelfDestruct = False
isBattleAlreadyActive = False
isAlreadyBackStirring = False
battleStartDelay = True
battleStartDelayTimer = None

class Point(tuple):
    def __new__(self, x, y):
        Point.x = property(operator.itemgetter(0))
        Point.y = property(operator.itemgetter(1))
        return tuple.__new__(Point, (x, y))

class CropArea(tuple):
    def __new__(self, x, y, xs, ys):
        CropArea.x = property(operator.itemgetter(0))
        CropArea.y = property(operator.itemgetter(1))
        CropArea.xs = property(operator.itemgetter(2))
        CropArea.ys = property(operator.itemgetter(3))
        return tuple.__new__(CropArea, (x, y, xs, ys))

class CropProperty(tuple):
    def __new__(self, name: str, area: CropArea, clickPos: Point, willClick: bool, expectedStrs: [[str]], clickWaitTime: int):
        CropProperty.name = property(operator.itemgetter(0))
        CropProperty.area = property(operator.itemgetter(1))
        CropProperty.clickPos = property(operator.itemgetter(2))
        CropProperty.willClick = property(operator.itemgetter(3))
        CropProperty.expectedStrs = property(operator.itemgetter(4))
        CropProperty.clickWaitTime = property(operator.itemgetter(5))
        return tuple.__new__(CropProperty, (name, area, clickPos, willClick, expectedStrs, clickWaitTime))

class Screen():

    def __init__(self, screenStep: const.ScreenStep, crops: [CropProperty], allowedRetryCount: int):
        self.screenStep = screenStep
        self.crops = crops
        self.allowedRetryCount = allowedRetryCount
        self.retryCount = 0

    def checkSatisfy(self, frame) -> bool:
        for crop in self.crops:
            crop_frame = frame[crop.area.y:crop.area.ys, crop.area.x:crop.area.xs]
            low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
            for expStrs in crop.expectedStrs:
                if low_txt not in expStrs:
                    return False
                pass
        return True
    
    def executeClick(self):
        for crop in self.crops:
            if crop.willClick:
                InputTrigger.mouseClick(getCorrectPos(crop.clickPos))
                time.sleep(crop.clickWaitTime)

    def addFailCount(self) -> bool:
        self.retryCount += 1
        if self.retryCount >= self.allowedRetryCount:
            return False
        return True
        


def bot():

    global isAlreadySelfDestruct
    global isBattleAlreadyActive
    global isAlreadyBackStirring
    global battleStartDelay
    global battleStartDelayTimer

    login_crops = [
        CropProperty(
            "Login Button",
            CropArea(const.login_label_width_start, const.login_label_height_start, const.login_label_width_end, const.login_label_height_end),
            Point(const.login_label_trigger_pos_x, const.login_label_trigger_pos_y),
            True,
            [["login","log in", "log ln", "logln"]],
            5
        )
    ]
    LoginScreen = Screen(const.ScreenStep.Login, login_crops, 30)

    welcome_crops = [
        CropProperty(
            "Welcome Promo Close Button",
            CropArea(const.welcome_promo_label_width_start, const.welcome_promo_label_height_start, const.welcome_promo_label_width_end, const.welcome_promo_label_height_end),
            Point(const.welcome_promo_label_trigger_pos_x, const.welcome_promo_label_trigger_pos_y),
            True,
            [["close", "c1ose", "ciose"]],
            1
        )
    ]
    WelcomeScreen = Screen(const.ScreenStep.WelcomeScreen, welcome_crops, 30)
    

    mainmenu_challenge_crops = [
        CropProperty(
            "Mainmenu Challenge Complete OK Button",
            CropArea(const.mainmenu_challenge_complete_ok_width_start, const.mainmenu_challenge_complete_ok_height_start, const.mainmenu_challenge_complete_ok_width_end, const.mainmenu_challenge_complete_ok_height_end),
            Point(const.mainmenu_challenge_complete_ok_trigger_pos_x, const.mainmenu_challenge_complete_ok_trigger_pos_y),
            True,
            [["ok", "0k"]],
            1
        )
    ]
    ChallengeCompleteScreen = Screen(const.ScreenStep.ChallengeCompleteScreen, mainmenu_challenge_crops, 30)

    
    mainmenu_crops = [
        CropProperty(
            "Main Menu Battle Button",
            CropArea(const.mainmenu_battle_label_width_start, const.mainmenu_battle_label_height_start, const.mainmenu_battle_label_width_end, const.mainmenu_battle_label_height_end),
            Point(const.mainmenu_battle_label_trigger_pos_x, const.mainmenu_battle_label_trigger_pos_y),
            False,
            [["battle", "batt1e"]],
            1
        ),
        CropProperty(
            "Main Menu Select Mode Button",
            CropArea(const.mainmenu_select_mode_label_width_start, const.mainmenu_select_mode_label_height_start, const.mainmenu_select_mode_label_width_end, const.mainmenu_select_mode_label_height_end),
            Point(const.mainmenu_select_mode_label_trigger_pos_x, const.mainmenu_select_mode_label_trigger_pos_y),
            True,
            [["select mode", "selectmode", "se1ect mode"]],
            1
        )
    ]
    MainMenuScreen = Screen(const.ScreenStep.MainMenu, mainmenu_crops, 30)




    currentStep = const.ScreenStep.Login
    
    retry_count = 0

    
    def getMaxRetryCount(step):
        if step == const.ScreenStep.BattlePrepareScreen:
            return 800
        elif step == const.ScreenStep.InBattleNow:
            return 300
        elif step == const.ScreenStep.FinishBattleScreen:
            return 800   
        else:
            return 100



    def report():
        print("Current Step is:", [currentStep])
        print("Current Retry Count is:", retry_count)
        calloutLst = ["b", "g", "c", "x", "z"]
        callout = random.choice(list(calloutLst))
        InputTrigger.KeyPress(callout).start()
        InputTrigger.KeyPress("r").start()
    
    setInterval(20, report)

    d = d3dshot.create(capture_output='numpy')
    d.display = d.displays[1]
    d.capture(target_fps=10, region=(0, 0, const.screenWidth, const.screenHeight))
    time.sleep(1)

    while True:

        np_frame = d.get_latest_frame()
        prev_frame = d.get_frame(10)
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)

        # test_frame = frame[ in_battle_mini_map_height_start:in_battle_mini_map_height_end, in_battle_mini_map_width_start:in_battle_mini_map_width_end ]
        # cv2.imshow("TestCrop", test_frame)
        # text = pytesseract.image_to_string(test_frame, lang='eng')
        # print(text)

        if currentStep == const.ScreenStep.Login:
            screen = LoginScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.WelcomeScreen:
            screen = WelcomeScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.ChallengeCompleteScreen:
            screen = ChallengeCompleteScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.MainMenu:
            screen = MainMenuScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1


        # # elif currentStep == ScreenStep.MainMenu:
        # #     mainmenu_battle_label_frame = frame[mainmenu_battle_label_height_start:mainmenu_battle_label_height_end, mainmenu_battle_label_width_start:mainmenu_battle_label_width_end]
        # #     cv2.imshow("MainMenuBattleCrop", mainmenu_battle_label_frame)
        # #     text = pytesseract.image_to_string(mainmenu_battle_label_frame, lang='eng')
        # #     if text == "BATTLE":
        # #         InputTrigger.mouseClick(Settings().settings.shiftX + mainmenu_battle_label_trigger_pos_x, Settings().settings.shiftY + mainmenu_battle_label_trigger_pos_y)   
        # #         retry_count = 0
        # #         currentStep += 1
        # #         cv2.destroyWindow("MainMenuBattleCrop")
        # #     elif retry_count >= max_retry_count:
        # #         retry_count = 0
        # #         currentStep += 1
        # #         cv2.destroyWindow("MainMenuBattleCrop")
        # #     else:
        # #         retry_count += 1

        # elif currentStep == ScreenStep.MainMenu:
        #     mainmenu_challenge_complete_ok_frame = frame[const.mainmenu_challenge_complete_ok_height_start:const.mainmenu_challenge_complete_ok_height_end, const.mainmenu_challenge_complete_ok_width_start:const.mainmenu_challenge_complete_ok_width_end]
        #     # cv2.imshow("MainMenuChallengeCrop", mainmenu_challenge_complete_ok_frame)
        #     text_challenge = pytesseract.image_to_string(mainmenu_challenge_complete_ok_frame, lang='eng')

        #     mainmenu_select_mode_label_frame = frame[const.mainmenu_select_mode_label_height_start:const.mainmenu_select_mode_label_height_end, const.mainmenu_select_mode_label_width_start:const.mainmenu_select_mode_label_width_end]
        #     # cv2.imshow("MainMenuBattleCrop", mainmenu_select_mode_label_frame)
        #     text_selectmode = pytesseract.image_to_string(const.mainmenu_select_mode_label_frame, lang='eng')

        #     if text_challenge == "OK":
        #         InputTrigger.mouseClick(getCorrectPos((const.mainmenu_challenge_complete_ok_trigger_pos_x, const.mainmenu_challenge_complete_ok_trigger_pos_y)))
        #         time.sleep(3)
        #         retry_count += 1
        #     if text_selectmode == "Select mode":
        #         InputTrigger.mouseClick(getCorrectPos((mainmenu_select_mode_label_trigger_pos_x, mainmenu_select_mode_label_trigger_pos_y)))
        #         time.sleep(1)
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("MainMenuBattleCrop")
        #         # cv2.destroyWindow("MainMenuChallengeCrop")
        #     elif retry_count >= getMaxRetryCount(currentStep):
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("MainMenuBattleCrop")
        #         # cv2.destroyWindow("MainMenuChallengeCrop")
        #     else:
        #         retry_count += 1

        # elif currentStep == ScreenStep.SelectMode:
        #     mode = random.choice(list(BattleMode))
        #     # mode = BattleMode.scrap
        #     # print(mode)
        #     if mode == BattleMode.scrap:
        #         InputTrigger.mouseClick(getCorrectPos((scrap_btn_trigger_pos_x, const.scrap_btn_trigger_pos_y)))
        #         time.sleep(1)
        #     elif mode == BattleMode.wire:
        #         InputTrigger.mouseClick(getCorrectPos((wire_btn_trigger_pos_x, wire_btn_trigger_pos_y)))
        #         time.sleep(1)
        #     elif mode == BattleMode.battery:
        #         InputTrigger.mouseClick(getCorrectPos((battery_btn_trigger_pos_x, battery_btn_trigger_pos_y)))
        #         time.sleep(1)
        #     else:
        #         InputTrigger.mouseClick(getCorrectPos((patrol_btn_trigger_pos_x, patrol_btn_trigger_pos_y)))
        #         time.sleep(1)
        #     retry_count = 0
        #     currentStep += 1

        # elif currentStep == ScreenStep.GetResourceMenu:
        #     get_resource_battle_label_frame = frame[get_resource_battle_label_height_start:get_resource_battle_label_height_end, get_resource_battle_label_width_start:get_resource_battle_label_width_end]
        #     get_resource_patrol_battle_label_frame = frame[get_resource_patrol_battle_label_height_start:get_resource_patrol_battle_label_height_end, get_resource_battle_label_width_start:get_resource_battle_label_width_end]
        #     # cv2.imshow("GetResourceBattleCrop", get_resource_battle_label_frame)
        #     # cv2.imshow("GetResourcePatrolBattleCrop", get_resource_patrol_battle_label_frame)
        #     text1 = pytesseract.image_to_string(get_resource_battle_label_frame, lang='eng')
        #     text2 = pytesseract.image_to_string(get_resource_patrol_battle_label_frame, lang='eng')
        #     if text1 == "BATTLE":
        #         InputTrigger.mouseClick(getCorrectPos((get_resource_battle_label_trigger_pos_x, get_resource_battle_label_trigger_pos_y)))
        #         time.sleep(1)
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("GetResourceBattleCrop")
        #         # cv2.destroyWindow("GetResourcePatrolBattleCrop")
        #     elif text2 == "BATTLE":
        #         InputTrigger.mouseClick(getCorrectPos((get_resource_patrol_battle_label_trigger_pos_x, get_resource_patrol_battle_label_trigger_pos_y)))
        #         time.sleep(1)
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("GetResourceBattleCrop")
        #         # cv2.destroyWindow("GetResourcePatrolBattleCrop")
        #     elif retry_count >= getMaxRetryCount(currentStep):
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("WelcomePromoCrop")
        #     else:
        #         retry_count += 1

        # elif currentStep == ScreenStep.BattlePrepareScreen:


        #     battle_type_title_label_frame = frame[battle_type_title_label_height_start:battle_type_title_label_height_end, battle_type_title_label_width_start:battle_type_title_label_width_end]
        #     # cv2.imshow("BattlePrepareCrop", battle_type_title_label_frame)
        #     text = pytesseract.image_to_string(battle_type_title_label_frame, lang='eng')
        #     # print(text)
        #     if text == "Assault" or text == "Encounter" or text == "Domination" or text == "Dominati"  or text == "Dominatio":
        #         InputTrigger.mouseClick(getCorrectPos((battle_type_title_label_trigger_pos_x, battle_type_title_label_trigger_pos_y)))
        #         time.sleep(1)
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("BattlePrepareCrop")
            
        #     elif retry_count >= getMaxRetryCount(currentStep):
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("BattlePrepareCrop")
        #     else:
        #         retry_count += 1




        # elif currentStep == ScreenStep.InBattleNow:
        #     # battle_lose_wait_frame = frame[battle_lose_wait_height_start:battle_lose_wait_height_end, battle_lose_wait_width_start:battle_lose_wait_width_end]
        #     # cv2.imshow("InBattleCrop", battle_lose_wait_frame)
        #     # ps_text = pytesseract.image_to_string(battle_lose_wait_frame, lang='eng')

        #     battle_lose_survivor_part_frame = frame[battle_lose_survivor_part_height_start:battle_lose_survivor_part_height_end, battle_lose_survivor_part_width_start:battle_lose_survivor_part_width_end]
        #     # cv2.imshow("InBattleSurvivorCrop", battle_lose_survivor_part_frame)
        #     surv_text = pytesseract.image_to_string(battle_lose_survivor_part_frame, lang='eng')
        #     # print(ps_text, surv_text)
            

        #     if (surv_text == "Survivor's parts"):
        #         retry_count = 0
        #         currentStep += 1
        #         # cv2.destroyWindow("InBattleCrop")
        #     elif retry_count >= getMaxRetryCount(currentStep):
        #         retry_count = 0
        #         currentStep += 1
        #     else:
        #         if battleStartDelay:
        #             DoBattleNow()
        #         else:
                    
        #             InputTrigger.KeyPress("t").start()

        #             test_frame = frame[ in_battle_mini_map_height_start:in_battle_mini_map_height_end, in_battle_mini_map_width_start:in_battle_mini_map_width_end ]
        #             hsv = cv2.cvtColor(test_frame, cv2.COLOR_BGR2HSV)
        #             lower_red = np.array([0,180,180])
        #             upper_red = np.array([10,255,255])
        #             mask = cv2.inRange(hsv, lower_red, upper_red)
        #             # cv2.imshow("MiniMap", mask)
        #             if cv2.countNonZero(mask) > 10:
        #                 executeOrder66()
                
        #             front_frame = np_frame[in_battle_front_view_height_start:in_battle_front_view_height_end, in_battle_front_view_width_start:in_battle_front_view_width_end]
        #             prev_front_frame = prev_frame[in_battle_front_view_height_start:in_battle_front_view_height_end, in_battle_front_view_width_start:in_battle_front_view_width_end]

        #             comp = cv2.absdiff(front_frame, prev_front_frame)
        #             # cv2.imshow("Comp", comp)
        #             res = comp.astype(np.uint8)
        #             percentage = (np.count_nonzero(res) * 100) / res.size
        #             # print(percentage)
        #             if percentage < 85:
        #                 # print(isAlreadyBackStirring)
        #                 backStir()

        #             health_frame = frame[ in_battle_health_digit_height_start:in_battle_health_digit_height_end, in_battle_health_digit_width_start:in_battle_health_digit_width_end ]
        #             # cv2.imshow("TestCrop", health_frame)
        #             a = pytesseract.image_to_string(health_frame)
        #             try:
        #                 inta = int(a)
        #                 if (inta <= 200):
        #                     selfDesctruct()
        #             except ValueError:
        #                 # print(ValueError)
        #                 pass

        #             retry_count += 1

        # elif currentStep == ScreenStep.DeathWaiting:

        #     currentStep += 1

        # elif currentStep == ScreenStep.FinishBattleScreen:
            

        #     finish_battle_close_label_frame = frame[finish_battle_close_label_height_start:finish_battle_close_label_height_end, finish_battle_close_label_width_start:finish_battle_close_label_width_end]
        #     # cv2.imshow("FinishBattleCloseCrop", finish_battle_close_label_frame)
        #     text = pytesseract.image_to_string(finish_battle_close_label_frame, lang='eng')
        #     if text == "Close":
                
        #         battleEnded()
        #         InputTrigger.mouseClick(getCorrectPos((finish_battle_close_label_trigger_pos_x, finish_battle_close_label_trigger_pos_y)))
        #         time.sleep(1)
        #         retry_count = 0
        #         currentStep = ScreenStep.MainMenu
        #         # cv2.destroyWindow("FinishBattleCloseCrop")
        #     elif retry_count >= getMaxRetryCount(currentStep):
        #         retry_count = 0
        #         currentStep = ScreenStep.MainMenu
        #         # cv2.destroyWindow("FinishBattleCloseCrop")
        #     else:
        #         retry_count += 1

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            d.stop()
            cv2.destroyAllWindows()
            break


import sched

import time, threading

StartTime=time.time()


class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

destructTimer = None

def destructComplete():
    global destructTimer
    global isAlreadySelfDestruct
    InputTrigger.keyRelease("m")
    isAlreadySelfDestruct = True
    destructTimer.cancel()


def selfDesctruct():
    global destructTimer
    global isAlreadySelfDestruct
    if isAlreadySelfDestruct == False:
        InputTrigger.keyHold("m")
        destructTimer = threading.Timer(5.0, destructComplete )
        destructTimer.start()
        
def battleEnded():
    
    global stirInterval
    global isAlreadySelfDestruct
    global isBattleAlreadyActive
    global isAlreadyBackStirring
    global battleStartDelay

    stirInterval.cancel()
    battleStartDelay = True
    isBattleAlreadyActive = False
    isAlreadySelfDestruct = False
    isAlreadyBackStirring = False
    InputTrigger.keyRelease("w")
    InputTrigger.keyRelease("a")
    InputTrigger.keyRelease("s")
    InputTrigger.keyRelease("d")
    InputTrigger.keyRelease("m")


backStirTimer1 = None
backStirTimer2 = None
backStirTimer3 = None
backStirTimer4 = None

backStirDirection = "a"

def backStir3():
    global backStirDirection
    global backStirTimer2
    global isAlreadyBackStirring

    backStirTimer2.cancel()
    isAlreadyBackStirring = False

def backStir2():
    global backStirTimer1
    global backStirTimer2
    backStirTimer1.cancel()
    InputTrigger.keyHold("w")
    backStirTimer2 = threading.Timer(3, backStir3)
    backStirTimer2.start()
        
def backStir():
    # print("<< In Battle >> Backing")
    global backStirDirection
    global backStirTimer1
    global isAlreadyBackStirring
    if isAlreadyBackStirring:
        pass
    else:
        isAlreadyBackStirring = True
        InputTrigger.keyRelease("w")
        InputTrigger.keyRelease("a")
        InputTrigger.keyRelease("s")
        InputTrigger.keyRelease("d")
        moveLst = ["a", "d"]
        # ranPara = random.choice(moveLst)
        backStirDirection = random.choice(moveLst)
        InputTrigger.KeyPress("s", 2.5).start()

        InputTrigger.KeyPress(backStirDirection, 1.6).start()

        backStirTimer1 = threading.Timer(2.65, backStir2)
        backStirTimer1.start() 
        
lastStir = "a"

def stirringHorizontal():
    # print("<< In Battle >> Stirring")
    global lastStir
    global isAlreadyBackStirring
    if isAlreadyBackStirring:
        pass
    else:
        InputTrigger.keyRelease("a")
        InputTrigger.keyRelease("d")
        if lastStir == "a":
            InputTrigger.KeyPress("d", 0.3).start()
            lastStir = "d"
        else:
            InputTrigger.KeyPress("a", 0.3).start()
            lastStir = "a"

def executeOrder66():
    # print("<< In Battle >> Attack")
    InputTrigger.KeyPress("1").start()

def delayBattleStart():
    global stirInterval
    global battleStartDelay
    global battleStartDelayTimer
    battleStartDelay = False
    battleStartDelayTimer.cancel()
    
    stirInterval = setInterval(6, stirringHorizontal)

stirInterval = None

def DoBattleNow():
    global isAlreadySelfDestruct
    global isBattleAlreadyActive
    global battleStartDelayTimer
    if isBattleAlreadyActive:
        # print("Battle Happening")
        pass
    else:
        isBattleAlreadyActive = True
        battleStartDelayTimer = threading.Timer(18, delayBattleStart)
        battleStartDelayTimer.start() 
        InputTrigger.keyHold("w")


