from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button

class Page_layout(PageLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.btn1=Button(
            text="btn1"
        )
        self.add_widget(self.btn1)

        self.btn2 = Button(
            text="btn2"
        )
        self.add_widget(self.btn2)

        self.btn3 = Button(
            text="btn3"
        )
        self.add_widget(self.btn3)



class DemoApp(App):
    def build(self):
        return Page_layout()

DemoApp().run()