import cv2
import pyautogui
import numpy as np

def findDistance(contour):
    max_y = -1
    min_x = 1000
    for point in contour:
        x = point[0][0]
        y = point[0][1]
        if min_x >x:
            min_x =x
        if max_y <y:
            max_y = y
    return min_x,max_y

while True :
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)

    lower = np.array([0,0,0])
    upper = np.array([120, 120,120])
    mask_sub = cv2.inRange(image,lower,upper)
    print(image.shape)
    # cv2.imshow('image',image)
    # cv2.imshow('mask_sub', mask_sub)
    mask_sub = mask_sub[int (768/11):int(768/2.6),int (768/11)+110:int(768/1.2)]
    image = cv2.resize(image,(300,300))
    cv2.imshow('in_memory_to_disk.png', image)

    kernel = np.ones((4,4))
    mask_sub = cv2.erode(mask_sub,kernel)
    kernel = np.ones((4, 4))
    mask_sub = cv2.dilate(mask_sub,kernel)

    mask_sub = cv2.resize(mask_sub,(300,300))

    _ , contours,hierarchy =cv2.findContours(mask_sub,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        tmp_c = contours[0]
        min_distance =1000
        max_height =-1
        for contour in contours:
            min_x,max_y=findDistance(contour)
            if min_distance > min_x:
                min_distance = min_x
                max_height = max_y
        print('mindis',min_distance)

        if min_distance < (20+0.01*max_height):
            pyautogui.press(' ')
        print('lencontour',len(contours))

        res = cv2.drawContours(mask_sub,contours,-1,(255),2)
    else:
        res = mask_sub
    cv2.imshow('result',res)
    cv2.waitKey(10)

