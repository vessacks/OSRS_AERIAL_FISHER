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

#works only in classic fixed rn
#take new green_fish image if you're having problems. alterantively, zoom out to the correct level. 
#do not move the knife! It won't look for it again until it hits the cut loop, which is supposed to be only a fallback

# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - Vessacks')


# initialize the Vision class
green_fish_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\green_fish.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
inv_fish_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\inv_fish.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
inv_tench_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\inv_tench.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
knife_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\knife.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)


#initialize the action class
knife_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\knife.png')
inv_fish_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\inv_fish.png')
inv_tench_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\inv_tench.png')
green_fish_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\aerial fisher\\green_fish.png')

GREEN_FISH_THRESHOLD = .6
KNIFE_THRESHOLD = .85
INV_FISH_THRESHOLD = .93
INV_TENCH_THRESHOLD = .98


def speed():
    speed = np.random.normal(.7,.3)
    while speed > .85 or speed < .6:
        speed = np.random.normal(.75,.08)
    return speed

#note: this is a stronger tick dropper than usual. it will drop up to 5 seconds. 
def tick_dropper(odds=400):
    if np.random.randint(0,odds) == 1:
        
        drop = np.random.uniform(.6,5)
        print('tick dropper! sleeping %s' %drop)
        time.sleep(drop)
    return

def wait():
    wait = (.1 + abs(np.random.normal(0,.05)))
    return wait


def fish_n_cut():
    loop_time = time.time()
    green_fish_click_time = time.time()
    green_fish_bestPoint_OLD = []      
    green_fish_confidence_OLD = 1 
    cycle_even = False
    cutting = False
    while True:
        if green_fish_confidence_OLD > .85: #ie if the previous fish was really green (ie .85 or higher confidence), wait for what will be two ticks (minus .5s find +move+wait+click time) then proceed to finding
            two_tick_wait =np.random.normal(1.5,.08) #.8,.08 works well
            while time.time() - green_fish_click_time < two_tick_wait:
                pass
            timing_belt = two_tick_wait +.5 #we add the .5 because we expect about .5s of bullshit to happen between now and the click

        else: #if the previous fish was really blue (less than .85 confidence green fish), wait (waht will be) 3 ticks (after serachign, moving, and waiting time elapse)
            three_tick_wait = np.random.normal(2.5,.12) #1.3,.12 works well
            while time.time() - green_fish_click_time < three_tick_wait:
                pass
            timing_belt = three_tick_wait +.5 #we add the .5 because we expect about .5s of bullshit to happen between now and the click

        #this line below is left in for debugging if needed
        #pre_find_wait_click_time = time.time()

        #we find and click the green fish. simple as. 
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        green_fish_allPoints, green_fish_bestPoint, green_fish_confidence = green_fish_vision.find(screenshot, threshold = GREEN_FISH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        
        #this line below is left in for debugging if needed
        #fish_find_time = time.time() - pre_find_wait_click_time
        
        #if the best fish is an old fish, AND you didn't cut last cycle, the mouse is still hovering over it and you should just click the mouse again
        if green_fish_bestPoint == green_fish_bestPoint_OLD and cutting == False:
            best_fish_old_fish = True
            time.sleep(.5)
            tick_dropper()
            pyautogui.click()
            actual_wait_time = time.time() - green_fish_click_time
            green_fish_click_time = time.time()
        
        #if it's not this unusual case, then set up and click as usual
        else:
            best_fish_old_fish = False
            green_fish_screenPoint = wincap.get_screen_position(green_fish_bestPoint)
            tick_dropper()
            green_fish_click_point = green_fish_action.click(green_fish_screenPoint, speed = speed(), wait=wait(), no_post_click_wait= True)
            #this line below is left in for debugging if needed
            #move_wait_click_time = time.time() - pre_find_wait_click_time - fish_find_time
            actual_wait_time = time.time() - green_fish_click_time
            green_fish_click_time = time.time()

            

        #we can't look fast enough to cut fish every cycle. It's not that the cycle runs long if we cut, it's that looking for cuttable fish takes so long that we have to start shortly after the last cut action. Most of the fish found there will disappear next tick and we click the empty spaces
        #solution to cut time problem: only cut on even cycles, ie every other cycle, and when it was a non-green fish click.

        #this defines the fast cut condition
        if cutting == False and green_fish_confidence < .85: #ie we didn't cut last time and it was NOT a green fish click (ie it will take 3+ ticks to resolve)
            cutting = True
            #we're looking for knife
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            knife_allPoints, knife_bestPoint, knife_confidence = knife_vision.find(screenshot, threshold = KNIFE_THRESHOLD, debug_mode= 'rectangles', return_mode = 'allPoints + bestPoint + confidence')
            knife_screenpoint = wincap.get_screen_position(knife_bestPoint)
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()

            #we're looking for inv. fish
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            inv_fish_allPoints, inv_fish_bestPoint, inv_fish_confidence = inv_fish_vision.find(screenshot, threshold = INV_FISH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()

            #if we see inv. fish, we cut it up before the next click
            if inv_fish_confidence > INV_FISH_THRESHOLD:
                tick_dropper()
                knife_click = knife_action.click(knife_screenpoint, speed = speed(), wait=wait()-.02, tick_dropper_odds= 100)
                fish_screenpoint = wincap.get_screen_position(inv_fish_bestPoint)
                tick_dropper()
                fish_click = inv_fish_action.click(fish_screenpoint, speed = speed()-.1, wait=wait()-.02, no_post_click_wait = True, tick_dropper_odds= 100)
            
            #we're looking for inv. tench
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            inv_tench_allPoints, inv_tench_bestPoint, inv_tench_confidence = inv_tench_vision.find(screenshot, threshold = INV_TENCH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()

            #if we see inv. tench, cut it up before the next click
            if inv_tench_confidence > INV_TENCH_THRESHOLD:
                knife_click = knife_action.click(knife_screenpoint, speed = speed(), wait=wait()-.02, tick_dropper_odds= 100)
                tench_screenpoint = wincap.get_screen_position(inv_tench_bestPoint)
                tick_dropper()
                tench_click = inv_tench_action.click(tench_screenpoint, speed = speed()-.1, wait=wait()-.02, no_post_click_wait = True, tick_dropper_odds= 100)

        else: #we're not cutting this cycle, but we still have to look for inv_fish and inv_tench to make sure we're not full inventory. This could theoretically be removed if you trusted the cut condition to cut enough (it only cuts at most 2 per call)
            #we're looking for inv. fish
            cutting = False
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            inv_fish_allPoints, inv_fish_bestPoint, inv_fish_confidence = inv_fish_vision.find(screenshot, threshold = INV_FISH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()

            #we're looking for inv. tench
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            inv_tench_allPoints, inv_tench_bestPoint, inv_tench_confidence = inv_tench_vision.find(screenshot, threshold = INV_TENCH_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            
            if len(inv_fish_allPoints + inv_tench_allPoints) > 20:
                print('at least 21 fish, exiting fishloop')
                break


        #debuggery
        print('cutting? %s | intended wait %ss |actual wait %s |green_fish_conf %s |num inv_fish %s conf. %s |num inv_tench %s conf. %s' % (cutting, round(timing_belt,2), round(actual_wait_time,2), round(green_fish_confidence,2), len(inv_fish_allPoints), round(inv_fish_confidence,3), len(inv_tench_allPoints), round(inv_tench_confidence,3)))
        #print('timing_belt debug | timing_belt %s | fish_find_time %s | move_wait_click_time %s | TOTAL TIME STALL %s | cutting? %s' %(timing_belt, fish_find_time, move_wait_click_time, timing_belt + fish_find_time + move_wait_click_time, cutting))


        #the new fish becomes the old fish
        green_fish_bestPoint_OLD = green_fish_bestPoint    
        green_fish_confidence_OLD = green_fish_confidence
        
        breakroller()
        #defunct
        '''
        #the even cycle becomes the odd cycle
        if cycle_even == True:
            cycle_even = False
        
        else: cycle_even = True
        pass
        '''
#we should not  have to use this cutloop much anymore. I leave it in  as a failsafe for fuckups. 
def cut_backup():
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

    tick_dropper()
    knife_click = knife_action.click(knife_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
    time.sleep(abs(np.random.normal(.1,.02)))
    fish_screenpoint = wincap.get_screen_position(inv_fish_bestPoint)
    tick_dropper()
    fish_click = inv_fish_action.click(fish_screenpoint, speed = speed()-.15, wait=wait(), tick_dropper_odds= 100)
    time.sleep(21 + abs(np.random.normal(0,.8)))

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
    if breakroll := np.random.random() < .000666: #this is about 1 in 1500. I figure I run the loop 3000 times per hour
        sleep_time = np.random.random() * 220
        print('sleeping for %s out of a possible 220 seconds' % sleep_time)
        wind_mouse(pyautogui.position()[0], pyautogui.position()[1], 0,0)
        time.sleep(sleep_time)

quit_after = float(input('please enter the number of seconds to run for, then press enter. 1h = 3600s, 6h = 21600'))
runStart = time.time()
while True:
    fish_n_cut()
    cut_backup()
    breakroller()
    runTime = time.time() - runStart
    if runTime > quit_after:
        print('finished after running for %s seconds' % runTime)
        exit()
    print('runtime = %s | seconds remaining = %s' %(runTime, (quit_after - runTime)))
    

