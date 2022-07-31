from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Grid_layout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows=4
        self.cols=1

        self.l1=Label(
            text="press button1"
        )
        self.b1=Button(
            text="Button1",
            background_color=(40,120,0,1),
            color=(.1,.2,.3,1)
        )

        self.l2 = Label(
            text="press button2"
        )
        self.b2 = Button(
            text="Button2",
            background_color=(40, 120, 0, 1),
            color=(.1, .2, .3, 1)
        )

        self.add_widget(self.l1)
        self.add_widget(self.b1)
        self.add_widget(self.l2)
        self.add_widget(self.b2)

class DemoApp(App):
    def build(self):
        return Grid_layout()

DemoApp().run()
