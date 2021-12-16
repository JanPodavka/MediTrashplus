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
from kivymd.uix.dialog import MDDialog


class LoginWindow(Screen):

    def login_write(self):
        app = MDApp.get_running_app()
        with open('data/reg_remember_user.txt') as f:
            lines = f.readlines()
        if len(lines) > 0:
            for line in lines:
                udaje = line.split(" ")
            self.ids['name'].text = udaje[0]
            self.ids['password'].text = udaje[1]
            self.ids['log_remember_user'].active = True

    def login_remember_user(self):
        app = MDApp.get_running_app()
        if(self.ids['log_remember_user'].active):
            ulozit = [self.ids['name'].text,self.ids['password'].text]
            f = open("data/reg_remember_user.txt", "w")
            f.write(' '.join(ulozit))
            f.close()
        else:
            f = open("data/reg_remember_user.txt", "w")
            f.write("")
            f.close()

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
                self.ids['password'].helper_text = ""
                self.ids['password'].error = False

                return True
        self.ids['password'].error = True
        self.ids['password'].helper_text = "Zadejte správné údaje"
        return False

    def login_clear_input(self):
        self.ids['name'].text = ""
        self.ids['password'].text = ""
        self.ids['log_remember_user'].active = False


class MainWindow(Screen):
    pass

class RegistrationWindow(Screen):

    def reg_check(self):

        def reg_ico_validity(ico):
            if len(ico) != 8:
                return -1
            try:
                digits = map(int, list(ico.rjust(8, "0")))
            except ValueError:
                return -1
            remainder = sum([digits[i] * (8 - i) for i in range(7)]) % 11
            cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
            if digits[7] != cksum:
                return -1
            return 1

        app = MDApp.get_running_app()
        reg_validity = 1
        #jmeno
        if self.ids['reg_name'].text == "":
            self.ids['reg_error_name'].text = "* Povinné pole"
            reg_validity = 0
        #ico
        if self.ids['reg_ico'].text == "":
            self.ids['reg_error_ico'].text = "* Povinné pole"
            reg_validity = 0
        #elif reg_ico_validity(self.ids['reg_ico'].text) != 1:
        #    self.ids['reg_error_ico'].text = "* Nevalidni ICO"
        #    reg_validity = False
        #adresa
        if self.ids['reg_address'].text == "":
            self.ids['reg_error_address'].text = "* Povinné pole"
            reg_validity = 0
        #telefoni cislo
        if self.ids['reg_number'].text == "":
            self.ids['reg_error_number'].text = "* Povinné pole"
            reg_validity = 0
        elif len(self.ids['reg_number'].text) != 9:
            self.ids['reg_error_number'].text = "* Neplatné číslo"
            self.ids['reg_number'].text = ""
            reg_validity = 0
        elif not self.ids['reg_number'].text.isdecimal():
            self.ids['reg_error_number'].text = "* Neplatné číslo"
            self.ids['reg_number'].text = ""
            reg_validity = 0
        #heslo
        if self.ids['reg_password'].text == "":
           self.ids['reg_error_password'].text = "* Povinné pole"
           reg_validity = 0
        #heslo2
        if self.ids['reg_password_check'].text == "":
           self.ids['reg_error_password_check'].text = "* Povinné pole"
           reg_validity = 0
        if self.ids['reg_password_check'].text != self.ids['reg_password'].text:
                self.ids['reg_password_check'].text = ""
                self.ids['reg_password'].text = ""
                self.ids['reg_error_password'].text = "* Hesla se neshodují"
                reg_validity = 0
        return reg_validity

    def reg_clear_label(self):
        app = MDApp.get_running_app()
        self.ids['reg_name'].text = ""
        self.ids['reg_ico'].text = ""
        self.ids['reg_address'].text = ""
        self.ids['reg_number'].text = ""
        self.ids['reg_password'].text = ""
        self.ids['reg_password_check'].text = ""

    def reg_clear_error(self):
        self.ids['reg_error_name'].text = ""
        self.ids['reg_error_ico'].text = ""
        self.ids['reg_error_address'].text = ""
        self.ids['reg_error_number'].text = ""
        self.ids['reg_error_password'].text = ""
        self.ids['reg_error_password_check'].text = ""

    dialog = None
    def show_alert_reg(self):
        self.dialog = MDDialog(
            title="Úspěšná registrace",
            radius=[50, 7, 50, 7],
            size_hint=[0.4, 0.2],
            type="custom",
        )
        self.dialog.open()

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
