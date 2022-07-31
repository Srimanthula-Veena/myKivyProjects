from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class Float_layer(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.btn1=Button(
            text="btn1",
            size_hint=(0.4,0.4),
            pos_hint={"x":0.3,"y":0.2}
        )
        self.add_widget(self.btn1)

        self.btn2 = Button(
            text="btn2",
            size_hint=(0.2, 0.1),
            pos_hint={"x": 0.9, "y": 0.9}
        )
        self.add_widget(self.btn2)

class DemoApp(App):
    def build(self):
        return Float_layer()

DemoApp().run()