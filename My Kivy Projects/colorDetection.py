import cv2
import numpy as np
import time

frameWidth=640
frameHeight=480
cap=cv2.VideoCapture(0)
cap.set(3,frameWidth) #width id is 3
cap.set(4,frameHeight) #height id is 4
cap.set(10,150) # brightness

myColors=[[5,142,156,25,255,255],[51,164,97,158,255,255],[28,102,87,69,255,255]]
myColorValues=[[7,120,240],[240,69,7],[7,240,116]]
myColorNames=["Orange","Blue","Green"]

def findColor(img,myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # conerts img to HSV
    count = 0
    c=0
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])  # creating lower and upper limit array for hsv
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult, (x, y), 10,myColorValues[count], cv2.FILLED)
        cv2.putText(imgResult, myColorNames[count], (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    myColorValues[count])
        cv2.imshow("Output",imgResult)
        if(x!=0 and y!=0):
            c+=1
        return c,myColorNames[count]
        count += 1

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # gets all contour lines
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt) #gets area formed by contour lines
        if area>200:# tiny ones can be neglected
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)  # draw contours on canvas with blue color 2 thickness
            peri=cv2.arcLength(cnt,True)# gets arc length to determine corners True is bcz they r closed arcs
            approx=cv2.approxPolyDP(cnt,0.02*peri,True) #approximate corners points are determined
            x,y,w,h=cv2.boundingRect(approx)#gives the dimensions for a bounding box to cover shape
    return x + w // 2, y


while(True):
    success,im=cap.read()
    img=cv2.flip(im,1)
    imgResult=img.copy()
    c,k=findColor(img,myColors)
    if(c==1):
        print(k)
        #cv2.imshow('Output', imgResult)
        #time.sleep(4)
        #break
   # cv2.imshow('Output',imgResult)
    if cv2.waitKey(1)& 0xFF==ord('q'):
        break