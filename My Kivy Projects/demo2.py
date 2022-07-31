from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

class DemoApp(App):
    def build(self):
        layout=AnchorLayout(
            anchor_x='right',
            anchor_y='bottom'
        )
        btn1=Button(
            text="AnchorLayout demo",
            size_hint=(.2,.2),
            background_color=(0,0,255,1),
            color=(0.2,0.4,0.1,1)
        )
        layout.add_widget(btn1)
        return layout

DemoApp().run()
