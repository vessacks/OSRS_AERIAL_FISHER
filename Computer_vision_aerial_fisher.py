# aerial fisher 

import cv2 as cv
from cv2 import threshold
from cv2 import _InputArray_STD_BOOL_VECTOR
import numpy as np
import os
from windmouse import wind_mouse
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
from action import Action

# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - Vessacks')


# initialize the Vision class
green_fish_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\green_fish.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
inv_fish_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\inv_fish.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
knife_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\knife.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)


#initialize the action class
knife_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\knife.png')
inv_fish_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\inv_fish.png')
green_fish_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\green_fish.png')

GREEN_FISH_THRESHOLD = .6
KNIFE_THRESHOLD = .7
INV_FISH_THRESHOLD = .7

def fishloop():
    loop_time = time.time()       
    while True:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        green_fish_allPoints, green_fish_bestPoint, green_fish_confidence = green_fish_vision.find(screenshot, threshold = GREEN_FISH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        

        green_fish_screenPoint = wincap.get_screen_position(green_fish_bestPoint)
        green_fish_action.click(green_fish_screenPoint)
        
        if green_fish_confidence > .85: #ie if is really found a green fish, wait only one tick
            time.sleep(abs(np.random.normal(.6,.07)))
            
        else: #if if found a blue fish, wait 2 ticks
            time.sleep(abs(np.random.normal(1.2,.3)))

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()


        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        
        inv_fish_allPoints, inv_fish_bestPoint, inv_fish_confidence = inv_fish_vision.find(screenshot, threshold = INV_FISH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if len(inv_fish_allPoints) > 20:
            print('I see 21 fish, exiting fishloop')
            break

        print('FPS = %s | num_green_fish = %s / maxVal = %s | num_inv_fish = %s / maxVal = %s ' %(round(1/(time.time() - loop_time)),len(green_fish_allPoints), round(green_fish_confidence,2), len(inv_fish_allPoints), round(inv_fish_confidence,2)))
        loop_time = time.time()
        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()


def cut():
    print('cutting up the fish')
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    inv_fish_allPoints, inv_fish_bestPoint, inv_fish_confidence = inv_fish_vision.find(screenshot, threshold = INV_FISH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()        

    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    knife_allPoints, knife_bestPoint, knife_confidence = knife_vision.find(screenshot, threshold = KNIFE_THRESHOLD, debug_mode= 'rectangles', return_mode = 'allPoints + bestPoint + confidence')
    knife_screenpoint = wincap.get_screen_position(knife_bestPoint)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()        
    
    knife_click = knife_action.click(knife_screenpoint)
    time.sleep(abs(np.random.normal(.1,.02)))
    fish_screenpoint = wincap.get_screen_position(inv_fish_bestPoint)
    fish_click = inv_fish_action.click(fish_screenpoint)
    time.sleep(np.random.normal(21,.8))

    #this is if you want to click FAST
    '''
    for fish in inv_fish_allPoints:
        time.sleep(abs(np.random.normal(.1,.02)))
        knife_click = knife_action.click(knife_screenpoint)

        time.sleep(abs(np.random.normal(.1,.02)))
        fish_screenpoint = wincap.get_screen_position(fish)
        fish_click = inv_fish_action.click(fish_screenpoint)
    '''


def breakroller():
    if breakroll := np.random.random() < .09:
        sleep_time = np.random.random() * 220
        print('sleeping for %s out of a possible 200 seconds' % sleep_time)
        wind_mouse(pyautogui.position()[0], pyautogui.position()[1], 0,0)
        time.sleep(sleep_time)

quit_after = float(input('please enter the number of seconds to run for, then press enter. 1h = 3600s, 6h = 21600'))
runStart = time.time()
while True:
    fishloop()
    cut()
    breakroller()
    runTime = time.time() - runStart
    if runTime > quit_after:
        print('finished after running for %s seconds' % runTime)
        exit()
    print('runtime = %s | seconds remaining = %s' %(runTime, (quit_after - runTime)))
    

