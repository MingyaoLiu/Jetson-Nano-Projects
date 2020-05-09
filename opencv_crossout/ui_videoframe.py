from sys import platform

import d3dshot

import matplotlib.pyplot as plt
import time
import os
import cv2
import math

import east_recognition

import pytesseract

import enum
import random

import InputTrigger

from protobuf_settings import Settings



screenWidth = 1920
screenHeight = 1080


def getCorrectPos(pos):
    print((int(Settings().settings.shiftX + pos[0]), int(Settings().settings.shiftY + pos[1])))
    return (int(Settings().settings.shiftX + pos[0]), int(Settings().settings.shiftY + pos[1]))

class BattleMode(enum.IntEnum):
    scrap = 0
    wire = 1
    battery = 2
    patrol = 3




scrap_btn_width = 40
scrap_btn_height = 40
scrap_btn_trigger_pos_x = int(screenWidth / 2 - scrap_btn_width / 2)
scrap_btn_trigger_pos_y = int(screenHeight / 4 - scrap_btn_height / 2)

wire_btn_width = 30
wire_btn_height = 30
wire_btn_trigger_pos_x = int(screenWidth / 2 + 100 - wire_btn_width / 2)
wire_btn_trigger_pos_y = int(screenHeight / 4 - wire_btn_height / 2)

battery_btn_width = 30
battery_btn_height = 30
battery_btn_trigger_pos_x = int(screenWidth / 2 - 100 - battery_btn_width / 2)
battery_btn_trigger_pos_y = int(screenHeight / 4 - battery_btn_height / 2)

patrol_btn_width = 30
patrol_btn_height = 30
patrol_btn_trigger_pos_x = int(screenWidth / 2 - patrol_btn_width / 2)
patrol_btn_trigger_pos_y = int(screenHeight / 4 + 120 - patrol_btn_height / 2)


class ScreenStep(enum.IntEnum):
    Login = 0
    WelcomeScreen = 1
    MainMenu = 2
    SelectMode = 3
    GetResourceMenu = 4
    BattlePrepareScreen = 5
    InBattleNow = 6
    DeathWaiting = 7
    FinishBattleScreen = 8
    debug = 9



login_label_width = 70
login_label_width_start = int(screenWidth / 7.5 - login_label_width / 2)
login_label_width_end = int(screenWidth / 7.5 + login_label_width / 2)
login_label_height = 40
login_label_height_start = int(screenHeight / 2 - login_label_height / 2)
login_label_height_end = int(screenHeight / 2 + login_label_height / 2)
login_label_trigger_pos_x = int(login_label_width_start + login_label_width / 2)
login_label_trigger_pos_y = int(login_label_height_start + login_label_height / 2)

welcome_promo_label_width = 70
welcome_promo_label_width_start = int(screenWidth / 1.5 - welcome_promo_label_width / 2)
welcome_promo_label_width_end = int(screenWidth / 1.5 + welcome_promo_label_width / 2)
welcome_promo_label_height = 40
welcome_promo_label_height_start = int(screenHeight / 1.5 - welcome_promo_label_height / 2)
welcome_promo_label_height_end = int(screenHeight / 1.5 + welcome_promo_label_height / 2)
welcome_promo_label_trigger_pos_x = int(welcome_promo_label_width_start + welcome_promo_label_width / 2)
welcome_promo_label_trigger_pos_y = int(welcome_promo_label_height_start + welcome_promo_label_height / 2)

mainmenu_battle_label_width = 140
mainmenu_battle_label_width_start = int(screenWidth / 2 - mainmenu_battle_label_width / 2)
mainmenu_battle_label_width_end = int(screenWidth / 2 + mainmenu_battle_label_width / 2)
mainmenu_battle_label_height = 50
mainmenu_battle_label_height_start = int(screenHeight / 5.65 - mainmenu_battle_label_height / 2)
mainmenu_battle_label_height_end = int(screenHeight / 5.65 + mainmenu_battle_label_height / 2)
mainmenu_battle_label_trigger_pos_x = int(mainmenu_battle_label_width_start + mainmenu_battle_label_width / 2)
mainmenu_battle_label_trigger_pos_y = int(mainmenu_battle_label_height_start + mainmenu_battle_label_height / 2)

mainmenu_select_mode_label_width = 130
mainmenu_select_mode_label_width_start = int(screenWidth / 2 - mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_width_end = int(screenWidth / 2 + mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_height = 60
mainmenu_select_mode_label_height_start = int(screenHeight / 4 - mainmenu_select_mode_label_height / 2)
mainmenu_select_mode_label_height_end = int(screenHeight / 4 + mainmenu_select_mode_label_height / 2)
mainmenu_select_mode_label_trigger_pos_x = int(mainmenu_select_mode_label_width_start + mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_trigger_pos_y = int(mainmenu_select_mode_label_height_start + mainmenu_select_mode_label_height / 2)

get_resource_battle_label_width = 130
get_resource_battle_label_width_start = int(screenWidth / 3 - get_resource_battle_label_width / 2)
get_resource_battle_label_width_end = int(screenWidth / 3 + get_resource_battle_label_width / 2)
get_resource_battle_label_height = 60
get_resource_battle_label_height_start = int(screenHeight / 1.37 - get_resource_battle_label_height / 2)
get_resource_battle_label_height_end = int(screenHeight / 1.37 + get_resource_battle_label_height / 2)
get_resource_battle_label_trigger_pos_x = int(get_resource_battle_label_width_start + get_resource_battle_label_width / 2)
get_resource_battle_label_trigger_pos_y = int(get_resource_battle_label_height_start + get_resource_battle_label_height / 2)

get_resource_patrol_battle_label_height_start = int(screenHeight / 1.3 - get_resource_battle_label_height / 2)
get_resource_patrol_battle_label_height_end = int(screenHeight / 1.3 + get_resource_battle_label_height / 2)
get_resource_patrol_battle_label_trigger_pos_x = int(get_resource_battle_label_width_start + get_resource_battle_label_width / 2)
get_resource_patrol_battle_label_trigger_pos_y = int(get_resource_patrol_battle_label_height_start + get_resource_battle_label_height / 2)

battle_type_title_label_width = 240
battle_type_title_label_width_start = int(screenWidth / 12 + 5 - battle_type_title_label_width / 2)
battle_type_title_label_width_end = int(screenWidth / 12 + 5 + battle_type_title_label_width / 2)
battle_type_title_label_height = 60
battle_type_title_label_height_start = int(screenHeight / 13.5 - battle_type_title_label_height / 2)
battle_type_title_label_height_end = int(screenHeight / 13.5 + battle_type_title_label_height / 2)
battle_type_title_label_trigger_pos_x = int(battle_type_title_label_width_start + battle_type_title_label_width / 2)
battle_type_title_label_trigger_pos_y = int(battle_type_title_label_height_start + battle_type_title_label_height / 2)

battle_lose_wait_width = 32
battle_lose_wait_width_start = int(screenWidth / 2 - 112 - battle_lose_wait_width / 2)
battle_lose_wait_width_end = int(screenWidth / 2 - 112 + battle_lose_wait_width / 2)
battle_lose_wait_height = 32
battle_lose_wait_height_start = int(screenHeight / 1.33 - battle_lose_wait_height / 2)
battle_lose_wait_height_end = int(screenHeight / 1.33 + battle_lose_wait_height / 2)
battle_lose_wait_trigger_pos_x = int(battle_lose_wait_width_start + battle_lose_wait_width / 2)
battle_lose_wait_trigger_pos_y = int(battle_lose_wait_height_start + battle_lose_wait_height / 2)

battle_lose_survivor_part_width = 240
battle_lose_survivor_part_width_start = int(screenWidth- battle_lose_survivor_part_width)
battle_lose_survivor_part_width_end = int(screenWidth)
battle_lose_survivor_part_height = 50
battle_lose_survivor_part_height_start = int(screenHeight / 2.4 - battle_lose_survivor_part_height / 2)
battle_lose_survivor_part_height_end = int(screenHeight / 2.4 + battle_lose_survivor_part_height / 2)
battle_lose_survivor_part_trigger_pos_x = int(battle_lose_survivor_part_width_start + battle_lose_survivor_part_width / 2)
battle_lose_survivor_part_trigger_pos_y = int(battle_lose_survivor_part_height_start + battle_lose_survivor_part_height / 2)


finish_battle_close_label_width = 120
finish_battle_close_label_width_start = int(screenWidth / 5 * 3.25 - finish_battle_close_label_width / 2)
finish_battle_close_label_width_end = int(screenWidth / 5 * 3.25 + finish_battle_close_label_width / 2)
finish_battle_close_label_height = 50
finish_battle_close_label_height_start = int(screenHeight / 13 * 12.1 - finish_battle_close_label_height / 2)
finish_battle_close_label_height_end = int(screenHeight / 13 * 12.1 + finish_battle_close_label_height / 2)
finish_battle_close_label_trigger_pos_x = int(finish_battle_close_label_width_start + finish_battle_close_label_width / 2)
finish_battle_close_label_trigger_pos_y = int(finish_battle_close_label_height_start + finish_battle_close_label_height / 2)

finish_battle_battle_label_width = 140
finish_battle_battle_label_width_start = int(screenWidth / 5 * 4.1 - finish_battle_battle_label_width / 2)
finish_battle_battle_label_width_end = int(screenWidth / 5 * 4.1 + finish_battle_battle_label_width / 2)
finish_battle_battle_label_height = 50
finish_battle_battle_label_height_start = int(screenHeight / 13 * 12.1 - finish_battle_battle_label_height / 2)
finish_battle_battle_label_height_end = int(screenHeight / 13 * 12.1 + finish_battle_battle_label_height / 2)
finish_battle_battle_label_trigger_pos_x = int(finish_battle_battle_label_width_start + finish_battle_battle_label_width / 2)
finish_battle_battle_label_trigger_pos_y = int(finish_battle_battle_label_height_start + finish_battle_battle_label_height / 2)


mainmenu_challenge_complete_ok_width = 60
mainmenu_challenge_complete_ok_width_start = int(screenWidth / 2 + 110 - mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_width_end = int(screenWidth / 2 + 110 + mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_height = 40
mainmenu_challenge_complete_ok_height_start = int(screenHeight / 1.08 - mainmenu_challenge_complete_ok_height / 2)
mainmenu_challenge_complete_ok_height_end = int(screenHeight / 1.08 + mainmenu_challenge_complete_ok_height / 2)
mainmenu_challenge_complete_ok_trigger_pos_x = int(mainmenu_challenge_complete_ok_width_start + mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_trigger_pos_y = int(mainmenu_challenge_complete_ok_height_start + mainmenu_challenge_complete_ok_height / 2)

def bot():

    currentStep = ScreenStep.BattlePrepareScreen

    d = d3dshot.create(capture_output='numpy')
    d.display = d.displays[1]
    d.capture(target_fps=20, region=(0, 0, screenWidth, screenHeight))
    time.sleep(1)


    retry_count = 0
    max_retry_count = 500

    isIdleActive = False
    isDead = False

    while True:
        time.sleep(0.1)


        print(currentStep, retry_count)

        frame = d.get_latest_frame()
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # cv2.imshow("CrossML", frame)

        # test_frame = frame[ battle_lose_survivor_part_height_start:battle_lose_survivor_part_height_end, battle_lose_survivor_part_width_start:battle_lose_survivor_part_width_end ]
        # cv2.imshow("TestCrop", test_frame)
        # text = pytesseract.image_to_string(test_frame, lang='eng')
        # print(text)




        if currentStep == ScreenStep.Login:
            login_frame = frame[login_label_height_start:login_label_height_end, login_label_width_start:login_label_width_end]
            cv2.imshow("LoginCrop", login_frame)
            text = pytesseract.image_to_string(login_frame, lang='eng')
            print(text)
            if text == "Login" or text == "Log in":
                InputTrigger.mouseClick(getCorrectPos((login_label_trigger_pos_x,login_label_trigger_pos_y)))
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("LoginCrop")
            elif retry_count >= max_retry_count:
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("LoginCrop")
            else:
                retry_count += 1

        elif currentStep == ScreenStep.WelcomeScreen:
            welcome_promo_frame = frame[welcome_promo_label_height_start:welcome_promo_label_height_end, welcome_promo_label_width_start:welcome_promo_label_width_end]
            cv2.imshow("WelcomePromoCrop", welcome_promo_frame)
            text = pytesseract.image_to_string(welcome_promo_frame, lang='eng')
            if text == "Close":
                InputTrigger.mouseClick(getCorrectPos((welcome_promo_label_trigger_pos_x,welcome_promo_label_trigger_pos_y)))
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("WelcomePromoCrop")
            elif retry_count >= max_retry_count:
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("WelcomePromoCrop")
            else:
                retry_count += 1
        
        # elif currentStep == ScreenStep.MainMenu:
        #     mainmenu_battle_label_frame = frame[mainmenu_battle_label_height_start:mainmenu_battle_label_height_end, mainmenu_battle_label_width_start:mainmenu_battle_label_width_end]
        #     cv2.imshow("MainMenuBattleCrop", mainmenu_battle_label_frame)
        #     text = pytesseract.image_to_string(mainmenu_battle_label_frame, lang='eng')
        #     if text == "BATTLE":
        #         InputTrigger.mouseClick(Settings().settings.shiftX + mainmenu_battle_label_trigger_pos_x, Settings().settings.shiftY + mainmenu_battle_label_trigger_pos_y)   
        #         retry_count = 0
        #         currentStep += 1
        #         cv2.destroyWindow("MainMenuBattleCrop")
        #     elif retry_count >= max_retry_count:
        #         retry_count = 0
        #         currentStep += 1
        #         cv2.destroyWindow("MainMenuBattleCrop")
        #     else:
        #         retry_count += 1

        elif currentStep == ScreenStep.MainMenu:
            mainmenu_challenge_complete_ok_frame = frame[mainmenu_challenge_complete_ok_height_start:mainmenu_challenge_complete_ok_height_end, mainmenu_challenge_complete_ok_width_start:mainmenu_challenge_complete_ok_width_end]
            cv2.imshow("MainMenuChallengeCrop", mainmenu_challenge_complete_ok_frame)
            text_challenge = pytesseract.image_to_string(mainmenu_challenge_complete_ok_frame, lang='eng')

            mainmenu_select_mode_label_frame = frame[mainmenu_select_mode_label_height_start:mainmenu_select_mode_label_height_end, mainmenu_select_mode_label_width_start:mainmenu_select_mode_label_width_end]
            cv2.imshow("MainMenuBattleCrop", mainmenu_select_mode_label_frame)
            text_selectmode = pytesseract.image_to_string(mainmenu_select_mode_label_frame, lang='eng')

            if text_challenge == "OK":
                InputTrigger.mouseClick(getCorrectPos((mainmenu_challenge_complete_ok_trigger_pos_x, mainmenu_challenge_complete_ok_trigger_pos_y)))
                retry_count += 1
            if text_selectmode == "Select mode":
                InputTrigger.mouseClick(getCorrectPos((mainmenu_select_mode_label_trigger_pos_x, mainmenu_select_mode_label_trigger_pos_y)))
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("MainMenuBattleCrop")
                cv2.destroyWindow("MainMenuChallengeCrop")
            elif retry_count >= max_retry_count:
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("MainMenuBattleCrop")
                cv2.destroyWindow("MainMenuChallengeCrop")
            else:
                retry_count += 1

        elif currentStep == ScreenStep.SelectMode:
            # mode = random.choice(list(BattleMode))
            mode = BattleMode.scrap
            print(mode)
            if mode == BattleMode.scrap:
                InputTrigger.mouseClick(getCorrectPos((scrap_btn_trigger_pos_x, scrap_btn_trigger_pos_y)))
            elif mode == BattleMode.wire:
                InputTrigger.mouseClick(getCorrectPos((wire_btn_trigger_pos_x, wire_btn_trigger_pos_y)))
            elif mode == BattleMode.battery:
                InputTrigger.mouseClick(getCorrectPos((battery_btn_trigger_pos_x, battery_btn_trigger_pos_y)))
            else:
                InputTrigger.mouseClick(getCorrectPos((patrol_btn_trigger_pos_x, patrol_btn_trigger_pos_y)))
            currentStep += 1

        elif currentStep == ScreenStep.GetResourceMenu:
            get_resource_battle_label_frame = frame[get_resource_battle_label_height_start:get_resource_battle_label_height_end, get_resource_battle_label_width_start:get_resource_battle_label_width_end]
            get_resource_patrol_battle_label_frame = frame[get_resource_patrol_battle_label_height_start:get_resource_patrol_battle_label_height_end, get_resource_battle_label_width_start:get_resource_battle_label_width_end]
            cv2.imshow("GetResourceBattleCrop", get_resource_battle_label_frame)
            cv2.imshow("GetResourcePatrolBattleCrop", get_resource_patrol_battle_label_frame)
            text1 = pytesseract.image_to_string(get_resource_battle_label_frame, lang='eng')
            text2 = pytesseract.image_to_string(get_resource_patrol_battle_label_frame, lang='eng')
            if text1 == "BATTLE":
                InputTrigger.mouseClick(getCorrectPos((get_resource_battle_label_trigger_pos_x, get_resource_battle_label_trigger_pos_y)))
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("GetResourceBattleCrop")
                cv2.destroyWindow("GetResourcePatrolBattleCrop")
            elif text2 == "BATTLE":
                InputTrigger.mouseClick(getCorrectPos((get_resource_patrol_battle_label_trigger_pos_x, get_resource_patrol_battle_label_trigger_pos_y)))
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("GetResourceBattleCrop")
                cv2.destroyWindow("GetResourcePatrolBattleCrop")
            else:
                retry_count += 1

        elif currentStep == ScreenStep.BattlePrepareScreen:


            battle_type_title_label_frame = frame[battle_type_title_label_height_start:battle_type_title_label_height_end, battle_type_title_label_width_start:battle_type_title_label_width_end]
            cv2.imshow("BattlePrepareCrop", battle_type_title_label_frame)
            text = pytesseract.image_to_string(battle_type_title_label_frame, lang='eng')
            print(text)
            if text == "Assault" or text == "Encounter" or text == "Domination" or text == "Dominati"  or text == "Dominatio":
                InputTrigger.mouseClick(getCorrectPos((battle_type_title_label_trigger_pos_x, battle_type_title_label_trigger_pos_y)))
                retry_count = 0
                currentStep += 1
                # cv2.destroyWindow("BattlePrepareCrop")
            
            elif retry_count >= max_retry_count:
                retry_count = 0
                currentStep += 1
                # cv2.destroyWindow("BattlePrepareCrop")
            else:
                retry_count += 1




        elif currentStep == ScreenStep.InBattleNow:
            # battle_lose_wait_frame = frame[battle_lose_wait_height_start:battle_lose_wait_height_end, battle_lose_wait_width_start:battle_lose_wait_width_end]
            # cv2.imshow("InBattleCrop", battle_lose_wait_frame)
            # text = pytesseract.image_to_string(battle_lose_wait_frame, lang='eng')
            # print(text)
            # if text == "PS" :
            #     currentStep += 1
            #     cv2.destroyWindow("InBattleCrop")
            #     wrap(True, isIdleActive)
            #     isIdleActive = False
            # else:
            #     print("No TEXT")
            #     wrap(False, isIdleActive)
            #     isIdleActive = True
            battle_lose_survivor_part_frame = frame[battle_lose_survivor_part_height_start:battle_lose_survivor_part_height_end, battle_lose_survivor_part_width_start:battle_lose_survivor_part_width_end]
            cv2.imshow("InBattleCrop", battle_lose_survivor_part_frame)
            text = pytesseract.image_to_string(battle_lose_survivor_part_frame, lang='eng')
            print(text)
            if text == "Survivor's parts":
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("InBattleCrop")
                wrap(True, isIdleActive)
                isIdleActive = False
            elif retry_count >= max_retry_count:
                retry_count = 0
                currentStep += 1
                cv2.destroyWindow("InBattleCrop")
            else:
                print("Not ENDING YET")
                wrap(False, isIdleActive)
                isIdleActive = True
                retry_count += 1

        elif currentStep == ScreenStep.DeathWaiting:
            currentStep += 1

        elif currentStep == ScreenStep.FinishBattleScreen:
            finish_battle_close_label_frame = frame[finish_battle_close_label_height_start:finish_battle_close_label_height_end, finish_battle_close_label_width_start:finish_battle_close_label_width_end]
            cv2.imshow("FinishBattleCloseCrop", finish_battle_close_label_frame)
            text = pytesseract.image_to_string(finish_battle_close_label_frame, lang='eng')
            if text == "Close":
                InputTrigger.mouseClick(getCorrectPos((finish_battle_battle_label_trigger_pos_x, finish_battle_battle_label_trigger_pos_y)))
                retry_count = 0
                currentStep = ScreenStep.MainMenu
                cv2.destroyWindow("FinishBattleCloseCrop")
            elif retry_count >= max_retry_count:
                retry_count = 0
                currentStep = ScreenStep.MainMenu
                cv2.destroyWindow("FinishBattleCloseCrop")
            else:
                retry_count += 1

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            d.stop()
            cv2.destroyAllWindows()
            break


import sched

import time, threading

StartTime=time.time()

def action() :
    print('action ! -> time : {:.1f}s'.format(time.time() - StartTime))

    keyLst = ["1", "2", "3", "4"]
    key1 = random.choice(keyLst)
    InputTrigger.keyPress(key1)
    
    # key2 = random.choice(keyLst)
    # InputTrigger.keyPress(key2)


def stirringHorizontal():
    InputTrigger.keyRelease("a")
    InputTrigger.keyRelease("d")
    moveLst = ["a", "d"]
    InputTrigger.keyHold(random.choice(moveLst))

def stirringFrontBack():
    InputTrigger.keyRelease("w")
    InputTrigger.keyRelease("s")
    moveLst = ["w", "s", "w", "w"]
    InputTrigger.keyHold(random.choice(moveLst))

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

def wrap(end, isIdleActive):
    print(isIdleActive)
    
    if end:
        InputTrigger.keyRelease("w")
        InputTrigger.keyRelease("a")
        InputTrigger.keyRelease("s")
        InputTrigger.keyRelease("d")

    elif isIdleActive:
        print("skip already looping")
    else:
        InputTrigger.keyHold("w")
        time.sleep(20)
        stirHori = setInterval(4, stirringHorizontal)
        stirVert = setInterval(15, stirringFrontBack)
        turret = setInterval(30, action)
        
        print('just after setInterval -> time : {:.1f}s'.format(time.time() - StartTime))

        t=threading.Timer(240,turret.cancel)
        t.start()
        t2=threading.Timer(240, stirHori.cancel)
        t2.start()
        t3=threading.Timer(240, stirVert.cancel)
        t3.start()