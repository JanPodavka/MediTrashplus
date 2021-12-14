from kivy import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen


class LoginWindow(Screen):
    pass


class MainWindow(Screen):
    pass

class RegistrationWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        screen = Builder.load_file("styly.kv")
        return screen


if __name__ == '__main__':
    MyApp().run()
