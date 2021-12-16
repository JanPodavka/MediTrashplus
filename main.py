from kivy import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.properties import StringProperty, ObjectProperty
import pyodbc


class LoginWindow(Screen):

    def login_user(self, loginText, passwordText):
        app = MDApp.get_running_app()
        # Otevři soubor
        app.cursor.execute('SELECT * FROM Zdravotnicke_zarizeni')
        for row in app.cursor:
            print(row)
            if self.ids['name'].text == row[3] and self.ids['password'].text == row[0]:
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

    def reg_check(self):
        app = MDApp.get_running_app()
        #jmeno
        if self.ids['reg_name'].text == "":
            self.ids['reg_error_name'].text = "* Povinné pole"
        #ico
        if self.ids['reg_ico'].text == "":
            self.ids['reg_error_ico'].text = "* Povinné pole"
        elif reg_ico_validity(self.ids['reg_ico'].text) != 1:
            self.ids['reg_error_ico'].text = "* Nevalidni ICO"
        #adresa
        if self.ids['reg_address'].text == "":
            self.ids['reg_error_address'].text = "* Povinné pole"
        #telefoni cislo
        if self.ids['reg_number'].text == "":
            self.ids['reg_error_number'].text = "* Povinné pole"
        elif len(self.ids['reg_number'].text) != 9:
            self.ids['reg_error_number'].text = "* Neplatné číslo"
            self.ids['reg_number'].text = ""
        #heslo
        if self.ids['reg_password'].text == "":
           self.ids['reg_error_password'].text = "* Povinné pole"
        #heslo2
        if self.ids['reg_password_check'].text == "":
           self.ids['reg_error_password_check'].text = "* Povinné pole"
        if self.ids['reg_password_check'].text != self.ids['reg_password'].text:
                self.ids['reg_password_check'].text = ""
                self.ids['reg_password'].text = ""
                self.ids['reg_error_password'].text = "* Hesla se neshodují"

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


class WindowManager(ScreenManager):
    pass


class MeditrashApp(MDApp):

    def build(self):
        usernameL = StringProperty(None)
        passwordL = StringProperty(None)
        cursor = ObjectProperty(None)

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        screen = Builder.load_file("styly.kv")

        # Načtení databáze

        connection_string = ("Driver={SQL Server Native Client 11.0};"
                             "Server=LAPTOP-JD638UP5;"
                             "Database=MediTrash;"
                             "Trusted_Connection=yes;")
        connection = pyodbc.connect(connection_string)
        self.cursor = connection.cursor()
        print(cursor)
        # cursor.execute('SELECT * FROM Zdravotnicke_zarizeni')
        # for row in cursor:
        # print(row)

        return screen


if __name__ == '__main__':
    MeditrashApp().run()
