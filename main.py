from kivy.lang import *
from kivy.uix.screenmanager import *
from kivymd.app import *
from kivymd.uix.screen import *


class LoginWindow(Screen):
    pass


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        screen = Builder.load_file("My.kv")
        return screen


if __name__ == '__main__':
    MyApp().run()
