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

    def reg_user(self, name):
        pass


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):

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
    MyApp().run()
