from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.graphics import Color,Rectangle

Window.clearcolor = (0.03, 0.73, 0.98, 1)

import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)  # width id is 3
cap.set(4, frameHeight)  # height id is 4
cap.set(10, 150)  # brightness

myColors = [[5, 142, 156, 25, 255, 255], [51, 164, 97, 158, 255, 255], [28, 102, 87, 69, 255, 255]]

myColorValues = [[7, 120, 240], [240, 69, 7], [7, 240, 116]]  # bgr

myColorNames=["Orange","Blue","Green"]

# [x,y,colorID]

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""


<MenuScreen>:
    FloatLayout:
    
        Image:
            source:'CRicon.png'
            size_hint_x: 0.2
            pos_hint: {"x":0.35, "y":0.35} 
            
        Button:
            text: "Play"
            background_color: 146, 164, 222,1
            size_hint: 0.6, 0.15
            color:0,0,0,1
            pos_hint: {"x":0.2, "y":0.55} 
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'paint'
        Button:
            text: "Test"
            background_color: 146, 164, 222, 1
            size_hint: 0.6, 0.15
            color:0,0,0,1
            pos_hint: {"x":0.2, "y":0.3}
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'test'

<PaintScreen>:





""")



# Declare both screens
class MenuScreen(Screen):
    pass


class PaintScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ps = GridLayout(rows=4, cols=1)
        self.myPts = []
        self.k = 0
        self.img1 = Image()
        ps.add_widget(self.img1)
        self.label=Label(
            text="Color",
            size=(790, 70),
            font_size='22dp',
            size_hint=(None, None),
            color=(0, 0, 0, 1)
        )
        with self.label.canvas.before:
            Color(255, 255, 255, 1)
            Rectangle(pos=self.label.pos, size=self.label.size)
        ps.add_widget(self.label)
        self.btn1 = Button(
            text="Clear",
            size_hint=(0.6, 0.15),
            background_color=(146, 164, 222, 1),
            color=(0, 0, 0, 1)
        )
        self.btn1.bind(on_press=self.clearPaint)
        self.btn2 = Button(
            text="Back",
            size_hint=(0.6, 0.15),
            background_color=(146, 164, 222, 1),
            color=(0, 0, 0, 1)
        )
        self.btn2.bind(on_press=self.changer1)
        ps.add_widget(self.btn1)
        ps.add_widget(self.btn2)
        self.add_widget(ps)
        # opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        # cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def changer1(self, *args):
        self.manager.current = 'menu'
        self.manager.transition.direction = 'right'

    def clearPaint(self, k):
        self.k = 1

    def findColor(self, img, imgResult, myColors, myColorValues):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # conerts img to HSV
        count = 0
        col=''
        newPts = []
        for color in myColors:
            lower = np.array(color[0:3])
            upper = np.array(color[3:6])  # creating lower and upper limit array for hsv
            mask = cv2.inRange(imgHSV, lower, upper)
            x, y = self.getContours(mask)
            cv2.circle(imgResult, (x, y), 10, myColorValues[count],
                       cv2.FILLED)  # circle at (x,y) with radius 1 and color blue
            if x != 0 and y != 0:
                newPts.append([x, y, count])
                col=myColorNames[count]
            count += 1
        return newPts,col

    def getContours(self, img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # gets all contour lines
        x, y, w, h = 0, 0, 0, 0
        for cnt in contours:
            area = cv2.contourArea(cnt)  # gets area formed by contour lines
            if area > 200:  # tiny ones can be neglected
                # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)  # draw contours on canvas with blue color 2 thickness
                peri = cv2.arcLength(cnt, True)  # gets arc length to determine corners True is bcz they r closed arcs
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
        if (self.k == 0):
            imgResult = img.copy()
            newPts,col= self.findColor(img, imgResult, myColors, myColorValues)
            if(col!=None):
                self.label.text = col
            if len(newPts) != 0:
                for npt in newPts:
                    self.myPts.append(npt)
            if len(self.myPts) != 0:
                self.drawOnCanvas(self.myPts, imgResult, myColorValues)
            buf = imgResult.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            # cv2.imshow('Output', imgResult)
            self.img1.texture = texture1
        else:
            self.k = 0
            imgResult = img.copy()
            self.myPts = []
            buf = imgResult.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            # cv2.imshow('Output', imgResult)
            self.img1.texture = texture1


class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ps = GridLayout(rows=4, cols=1)
        self.score = 0
        self.label=Label(
            text="Your Score : "+str(self.score),
            size=(790, 50),
            font_size='22dp',
            size_hint=(None, None)
        )
        ps.add_widget(self.label)
        self.img1 = Image()
        ps.add_widget(self.img1)
        self.label1 = Label(
            text="Color",
            size=(790, 60),
            font_size='22dp',
            size_hint=(None, None)
        )
        ps.add_widget(self.label1)
        self.btn1 = Button(
            text="Back",
            size_hint=(0.6, 0.15),
            background_color=(146, 164, 222, 1),
            color=(0, 0, 0, 1)
        )
        self.btn1.bind(on_press=self.changer1)
        ps.add_widget(self.btn1)
        self.add_widget(ps)


    def changer1(self, *args):
        self.manager.current = 'menu'
        self.manager.transition.direction = 'left'







class TestApp(App):

    def build(self):
        # Create the screen manager
        self.title = 'CoLorRusH'
        self.icon='CRicon.png'
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(PaintScreen(name='paint'))
        sm.add_widget(TestScreen(name='test'))

        return sm



TestApp().run()