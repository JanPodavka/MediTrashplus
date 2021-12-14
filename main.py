from kivy import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.properties import StringProperty


class LoginWindow(Screen):

    def login_user(self, loginText, passwordText):
        app = MDApp.get_running_app()
        app.usernameL = loginText
        app.passwordL = passwordText
        print(app.usernameL)
        print(app.passwordL)
        app.usernameL = self.ids['name'].text
        app.passwordL = self.ids['password'].text


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):

    def build(self):
        usernameL = StringProperty(None)
        passwordL = StringProperty(None)

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        screen = Builder.load_file("styly.kv")
        return screen


if __name__ == '__main__':
    MyApp().run()
