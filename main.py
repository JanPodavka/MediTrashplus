from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen


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
        print("Test")
        print("Test1")
        print("Test2")
        return screen


if __name__ == '__main__':
    MyApp().run()
