from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.graphics.texture import Texture

import cv2
import numpy as np


frameWidth=640
frameHeight=480
cap=cv2.VideoCapture(0)
cap.set(3,frameWidth) #width id is 3
cap.set(4,frameHeight) #height id is 4
cap.set(10,150) # brightness

myColors=[[5,142,156,25,255,255],[51,164,97,158,255,255],[28,102,87,69,255,255]]

myColorValues=[[7,120,240],[240,69,7],[7,240,116]] #bgr

myPts=[] #[x,y,colorID]

class Layout(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.rows=3
        self.cols=1
        self.img1 = Image()
        self.add_widget(self.img1)
        self.btn1 = Button(
            text="Clear",
            size_hint=(0.6, 0.15),
            background_color=(146, 164, 222,1),
            color=(0,0,0,1)
        )
        self.btn2 = Button(
            text="Back",
            size_hint=(0.6, 0.15),
            background_color=(146, 164, 222, 1),
            color = (0, 0, 0, 1)
        )
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        # opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        # cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def findColor(self, img, imgResult, myColors, myColorValues):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # conerts img to HSV
        count = 0
        newPts = []
        for color in myColors:
            lower = np.array(color[0:3])
            upper = np.array(color[3:6])  # creating lower and upper limit array for hsv
            mask = cv2.inRange(imgHSV, lower, upper)
            x, y = self.getContours(mask)
            cv2.circle(imgResult, (x, y), 10, myColorValues[count],cv2.FILLED)  # circle at (x,y) with radius 1 and color blue
            if x != 0 and y != 0:
                newPts.append([x, y, count])
            count += 1
        return newPts

    def getContours(self, img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  # gets all contour lines
        x, y, w, h = 0, 0, 0, 0
        for cnt in contours:
            area = cv2.contourArea(cnt)  # gets area formed by contour lines
            if area > 200:  # tiny ones can be neglected
                    # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)  # draw contours on canvas with blue color 2 thickness
                peri = cv2.arcLength(cnt,True)  # gets arc length to determine corners True is bcz they r closed arcs
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # approximate corners points are determined
                x, y, w, h = cv2.boundingRect(approx)  # gives the dimensions for a bounding box to cover shape
        return x + w // 2, y

    def drawOnCanvas(self, myPts, imgResult, myColorValues):
        for pt in myPts:
            cv2.circle(imgResult, (pt[0], pt[1]), 20, myColorValues[pt[2]], cv2.FILLED)

    def update(self, dt):
            # display image from cam in opencv window
        ret, img = self.capture.read()
            # cv2.imshow("CV2 Image", frame)
        img = cv2.flip(img, -1)
        imgResult = img.copy()
        newPts = self.findColor(img, imgResult, myColors, myColorValues)
        if len(newPts) != 0:
            for npt in newPts:
                myPts.append(npt)
        if len(myPts) != 0:
            self.drawOnCanvas(myPts, imgResult, myColorValues)
        buf = imgResult.tostring()
        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            # cv2.imshow('Output', imgResult)
        self.img1.texture = texture1


class CamApp(App):

    def build(self):
        return Layout()





if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()