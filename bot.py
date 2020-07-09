import pyautogui
from PIL import ImageGrab
import cv2 as cv
import numpy as np

'''Pointing to the game window and turning it into an active state'''

pyautogui.moveTo(1000,400,duration=1)
pyautogui.click()
pyautogui.keyDown('enter')
pyautogui.keyUp('enter')

position = 12

'''Main work cycle'''

while True:

    ball_list=[]
    player_left_list=[]
    player_right_list=[]

    base_screen = ImageGrab.grab(bbox=(360, 790, 600, 950)) #for monitors 1920 * 1080 pixels
    base_screen.save('base_screen.png')

    '''Search and list of ball coordinates'''

    img_rgb = cv.imread('base_screen.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('ball_template.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9 #template recognition accuracy
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        x = ((pt[0] + w, pt[1] + h)[0] - pt[0]) / 2 + pt[0]
        y = ((pt[0] + w, pt[1] + h)[1] - pt[1]) / 2 + pt[1]
        ball_list.append(y)

    '''Search for a player and record his coordinates'''

    template = cv.imread('player_template.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9 #template recognition accuracy
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        x = ((pt[0] + w, pt[1] + h)[0] - pt[0]) / 2 + pt[0]
        y = int(((pt[0] + w, pt[1] + h)[1] - pt[1]) / 2 + pt[1])
        print('Player:', x,y)
        player_left_list = [i for i in range(y-20, y)]
        player_right_list = [i for i in range(y, y + 20)]

    '''Logic of movement'''

    intersection_left_list = []
    for i in ball_list:
        for j in player_left_list:
            if i == j:
                intersection_left_list.append(i)
                break

    intersection_right_list = []
    for i in ball_list:
        for j in player_right_list:
            if i == j:
                intersection_right_list.append(i)
                break

    if not intersection_left_list:
        if (position<=11) and (position>=0):
            pyautogui.keyDown('d')
            pyautogui.keyUp('d')
            position += 1


    else:
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
        position+=1
        print("Right move")

    if not intersection_right_list:
            if position >= 13 and position <= 25:
                pyautogui.keyDown('a')
                pyautogui.keyUp('a')
                position -= 1
    else:
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
        position-=1
        print("Right move")

    print("Balls:",ball_list)





