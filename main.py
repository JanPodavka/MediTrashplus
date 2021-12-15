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
        #Otevři soubor
        with open('data/pass.txt') as f:
            lines = f.readlines()
        # porovnaj zda je v DTB (zatím txt)
        for line in lines:
            line = line.replace("\n", "")
            udaje = line.split(" ")
            if self.ids['name'].text == udaje[0] and self.ids['password'].text == udaje[1]:
                print("úspěšně přihlášeno")
                # Náhrání do údajů aktivnního uživatele
                app.usernameL = loginText
                app.passwordL = passwordText
                # Vymazání text inputů
                self.ids['name'].text = ""
                self.ids['password'].text = ""
                self.ids['password'].helper_text = ""
                self.ids['password'].error = False

                return True
        print("Špatné údaje")
        self.ids['password'].error = True
        self.ids['name'].text = ""
        self.ids['password'].text = ""
        self.ids['password'].helper_text = "Zadejte správné údaje"
        return False



class MainWindow(Screen):
    pass

class RegistrationWindow(Screen):

    def reg_user(self):
        app = MDApp.get_running_app()
        if self.ids['reg_name'].text == "":
            self.ids['reg_name'].error = True
            self.ids['reg_name'].text = "Povinný údaj"
        if self.ids['reg_password'].text != self.ids['reg_password_check']:
            self.ids['reg_password'].helper_text = ""
            self.ids['reg_password_check'].helper_text = ""
            self.ids['reg_password'].error = True
            self.ids['reg_password_check'].error = True

class WindowManager(ScreenManager):
    pass


class MeditrashApp(MDApp):

    def build(self):
        usernameL = StringProperty(None)
        passwordL = StringProperty(None)

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        screen = Builder.load_file("styly.kv")
        return screen


if __name__ == '__main__':
    MeditrashApp().run()
