from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image #import Image whn u have downloaded img with u

class kivy_UI(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=1
        self.rows=4

        self.img=Image(
            source="E:\\My codes\\OpenCV projects\\assets\\car.jfif"
        )
        self.add_widget(self.img)

        self.lab=Label(
            text="Enter Your name"
        )

        self.add_widget(self.lab)

        self.txt=TextInput(
            text="",font_size=40
        )
        self.add_widget(self.txt)

        self.btn=Button(
            text="Submit"
        )
        self.btn.bind(on_press=self.call_back)
        self.add_widget(self.btn)

        self.pop=Popup(
            title="Pop-Up display",
            size = (400 ,400 ),
            size_hint=(None,None),
            content=Label(
                text=""
            )
        )

    def call_back(self,ele):
        self.pop.content.text=self.txt.text
        self.pop.open()


class DemoApp(App):
    def build(self):
        return kivy_UI()

DemoApp().run()