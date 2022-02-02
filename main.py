from kivymd.uix.list import TwoLineListItem, IRightBodyTouch, TwoLineAvatarIconListItem, MDList
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
import pyodbc
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from datetime import date
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
import locale
from kivy.metrics import dp
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.text import Label
from kivy.lang.builder import Builder
from kivy.graphics import Line, Rectangle, Color
from fpdf import FPDF
from pathlib import Path
from matplotlib import pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg

_ACCEPTED_BAR_CAPS = {"round", "none", "square"}
_DEFAULT_THICKNESS = 10
_DEFAULT_CAP_STYLE = 'round'
_DEFAULT_PRECISION = 10
_DEFAULT_PROGRESS_COLOUR = (0, 0, 0, .3)
_DEFAULT_BACKGROUND_COLOUR = (0.26, 0.26, 0.26, 1)
_DEFAULT_MAX_PROGRESS = 100
_DEFAULT_MIN_PROGRESS = 0
_DEFAULT_WIDGET_SIZE = 200
_DEFAULT_TEXT_LABEL = Label(text="{}%", font_size=40)
_NORMALISED_MAX = 1
_NORMALISED_MIN = 0

locale.setlocale(locale.LC_TIME, "cs_CZ")

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    pass

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
            print(value)
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
            print(value)

class Send_checker(BoxLayout):
    pass

class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.thickness = 40
        self.label = CoreLabel(text="0%", font_size=self.thickness)
        self.texture_size = None
        self.refresh_text()
        self.draw()

    def draw(self):
        with self.canvas:
            self.canvas.clear()
            Color(0.26, 0.26, 0.26, .5)
            Ellipse(pos=self.pos, size=self.size)
            Color(.2, 0, 0, .5)
            Ellipse(pos=self.pos, size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized * 360))
            Color(0, 0, 0, .2)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))
            Color(1, 1, 1, 1)
            Rectangle(texture=self.label.texture, size=self.texture_size,
                      pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0],
                           self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))

    def refresh_text(self):
        self.label.refresh()
        self.texture_size = list(self.label.texture.size)
    def set_value(self, value):
        self.value = value
        self.label.text = str(int(self.value_normalized * 100)) + "%"
        self.refresh_text()
        self.draw()

class OdvozWindow(Screen):

    def on_leave(self, *args):
        self.ids.scroll.clear_widgets()

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        sql = 'SELECT nazev,o.id_odpad, SUM(mnozstvi) from Odpad o,Katalog_odpadu k WHERE o.id_odpad = k.id_odpad AND datum_odvozu IS NULL  AND id_zdravotnicke_zarizeni = ? GROUP BY nazev,o.id_odpad'
        val = app.usernameL
        app.cursor.execute(sql, val)
        for row in app.cursor:
            item = ListItemWithCheckbox(text=f"{row[0]}", secondary_text = f"{row[1]}",  tertiary_text=f"Váha: {row[2]} g")
            self.ids.scroll.add_widget(item)
        sql = 'SELECT * from Opravnena_osoba'
        app.cursor.execute(sql)
        osoby = []
        nazev_osob = []
        for row in app.cursor:
            osoby.append(row)
            nazev_osob.append(row[1])
        self.ids.drop_item.values = nazev_osob

    def send_trash(self):
        app = MDApp.get_running_app()
        if self.ids['drop_item'].text == "Vyberte osobu":
            self.ids.Send_error_mess.text = "* Povinné pole"
        else:
            self.ids.Send_error_mess.text = ""
            self.dialog = MDDialog(
                title="Opravdu si přejete odeslat",
                radius=[20, 20, 20, 20],
                size_hint=[.5, .6],
                type="custom",
                auto_dismiss=False,
                content_cls=Send_checker(),
                buttons=[
                    MDFlatButton(
                        text="Zpět",
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Odeslat",
                        on_release=self.get_active_check
                    ),
                ],
            )
            self.dialog.open()

    def get_active_check(self,*args):
        app = MDApp.get_running_app()
        sql = 'SELECT ico FROM Opravnena_osoba WHERE nazev = ?'
        val = self.ids['drop_item'].text
        app.cursor.execute(sql, val)
        opravnena_osoba = []
        for row in app.cursor:
            opravnena_osoba.append(row)
        for element in self.ids.scroll.children:
            if element.ids.check.active:
                sql = "UPDATE Odpad SET id_opravnena_osoba = (?), datum_odvozu = (?) WHERE id_odpad = (?) AND id_zdravotnicke_zarizeni = (?)"
                val = str(opravnena_osoba[0][0]),date.today().strftime("%d.%m.%Y"),element.secondary_text, app.usernameL
                app.cursor.execute(sql, val)
                app.cursor.commit()
        self.dialog.dismiss()
        for element in self.ids.scroll.children:
            element.ids.check.active = False

        self.ids.scroll.clear_widgets()
        sql = 'SELECT nazev,o.id_odpad, SUM(mnozstvi) from Odpad o ,Katalog_odpadu k WHERE o.id_odpad = k.id_odpad AND datum_odvozu IS NULL  AND id_zdravotnicke_zarizeni = ? GROUP BY nazev,o.id_odpad'
        val = app.usernameL
        app.cursor.execute(sql, val)
        for row in app.cursor:
            item = ListItemWithCheckbox(text=f"{row[0]}", secondary_text=f"{row[1]}", tertiary_text=f"Váha: {row[2]} g")
            self.ids.scroll.add_widget(item)

        Snackbar(
            text="Úspěšně odesláno",
            snackbar_x="10dp",
            snackbar_y="10dp",
            bg_color=(0, 0, 0, .2)
        ).open()

    def close_dialog(self,obj):
         self.dialog.dismiss()

class HistoryWindow(Screen):

    def on_leave(self, *args):
        self.table.clear_widgets()

    def on_pre_enter(self, *args):

        app = MDApp.get_running_app()
        SQL = "SELECT o.id, nazev, o.id_odpad, mnozstvi, kategorie, datum_uskladneni, ISNULL(datum_odvozu," \
              "'neodvezeno'),ISNULL(id_opravnena_osoba,'nepřiřazeno') FROM Odpad o, Katalog_odpadu k WHERE o.id_odpad = k.id_odpad AND id_zdravotnicke_zarizeni = (?) "
        val = app.usernameL
        data = app.cursor.execute(SQL, val)
        hist_data = []
        for row in data:
            if row[4] == 1:
                row[4] = "nebezpečné"
            else:
                row[4] = "bezpečné"

            hist_data.append(row)

        table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(.5, .6),
            use_pagination=True,
            rows_num=7,
            check=True,
            pagination_menu_height='240dp',
            pagination_menu_pos="auto",
           # background_color=[1, 1, 1, 1],
            column_data=[
                (" ID ", dp(20)),
                ("Název", dp(45)),
                ("Katalogoé číslo", dp(35)),
                ("Váha (g)", dp(25)),
                ("Kategorie", dp(45)),
                ("Datum uskladnění", dp(45)),
                ("Datum odvozu", dp(45)),
                ("IČO Odvozce", dp(45)),
            ],
            row_data=hist_data,
            sorted_on=" ID ",
            sorted_order="ASC"
        )
        self.ids['table'].add_widget(table)
        app.selected_rows = [" ", " ", " ", " ", " ", " ", " "]
        table.bind(on_check_press=self.on_check_press)

    def on_check_press(self, instance_table, current_row):
        #print(instance_table, current_row,instance_row)
        # app = MDApp.get_running_app()
        # app.selected_rows = instance_table.get_row_checks()
        # print("--------------všechny zvolené---------")
        print(instance_table.get_row_checks())
        pass

    def on_leave(self, *args):
        self.ids.table.clear_widgets()

    def removeSelectedRows(self, *args):
        app = MDApp.get_running_app()
        print(app.selected_rows)
        for row in app.selected_rows:
            SQL = "DELETE from Odpad where id = ? AND zdravotnicke_zarizeni_ico = ?"
            val = (row[0], app.usernameL)
            app.cursor.execute(SQL, val)
            app.cursor.commit()

        app.selected_rows = [" ", " ", " ", " ", " ", " ", " "]

class LoginWindow(Screen):

    def login_write(self):
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
        if (self.ids['log_remember_user'].active):
            ulozit = [self.ids['name'].text, self.ids['password'].text]
            f = open("data/reg_remember_user.txt", "w")
            f.write(' '.join(ulozit))
            f.close()
        else:
            f = open("data/reg_remember_user.txt", "w")
            f.write("")
            f.close()

    def login_show_password(self):
        self.ids['password'].password = not self.ids['password'].password
        if self.ids['password'].password:
            self.ids['lock_button'].icon = "eye-off"
        else:
            self.ids['lock_button'].icon = "eye"

    def login_user(self, loginText, passwordText):
        app = MDApp.get_running_app()
        # Otevři soubor
        app.cursor.execute('SELECT * FROM Zdravotnicke_zarizeni')
        for row in app.cursor:
            if self.ids['name'].text == row[1] and self.ids['password'].text == row[2]:
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

class StatisticWindow(Screen):
    def on_leave(self, *args):
        self.ids['graf1'].clear_widgets()
        self.ids['graf2'].clear_widgets()

    def on_pre_enter(self, *args):
        self.first_graph()

    def second_graph(self, *args):
        self.ids['graf1'].clear_widgets()
        self.ids['graf2'].clear_widgets()
        self.ids['neodvezeno'].background_color = [0, 0, 0, 0.5]
        self.ids['celkem'].background_color = [0, 0, 0, 0.3]
        app = MDApp.get_running_app()
        SQL = "SELECT o.id_odpad,SUM(mnozstvi) FROM Odpad o,Katalog_odpadu k WHERE o.id_odpad = k.id_odpad AND datum_odvozu IS NULL AND  id_zdravotnicke_zarizeni = ? GROUP BY o.id_odpad"
        val = (app.usernameL)
        data = app.cursor.execute(SQL, val)
        mnozstvi = []
        nazvy = []
        for row in data:
            nazvy.append(row[0])
            mnozstvi.append(row[1])
        plt.figure(3)
        plt.bar(nazvy, mnozstvi, color=(0, 0, 1, 0.6))
        plt.ylabel("Váha (g)")
        plt.xlabel("Kód odpadu")
        self.ids['graf1'].add_widget(FigureCanvasKivyAgg(plt.gcf()))
        plt.figure(4)
        SQL = "SELECT kategorie,SUM(mnozstvi) FROM 	Odpad o,Katalog_odpadu k WHERE o.id_odpad = k.id_odpad AND datum_odvozu IS NULL AND id_zdravotnicke_zarizeni = ? GROUP BY kategorie"
        val = (app.usernameL)
        data2 = app.cursor.execute(SQL, val)
        bezpecnost = []
        bezpecnost_name = []
        for row in data2:
            print(row)
            if row[0] == 1:
                bezpecnost.append("Bezpečný")
                bezpecnost_name.append(row[1])
            else:
                bezpecnost.append("Nebezpečný")
                bezpecnost_name.append(row[1])

        bar_bez = plt.bar(bezpecnost, bezpecnost_name)
        bar_bez[0].set_color('r')
        if len(bar_bez) > 1:
            bar_bez[1].set_color('g')

        plt.ylabel("Váha (g)")
        plt.xlabel("Kategorie")
        self.ids['graf2'].add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def first_graph(self,*args):
        self.ids['graf1'].clear_widgets()
        self.ids['graf2'].clear_widgets()
        self.ids['neodvezeno'].background_color = [0, 0, 0, 0.3]
        self.ids['celkem'].background_color = [0, 0, 0, 0.5]
        app = MDApp.get_running_app()
        SQL = "SELECT o.id_odpad,SUM(mnozstvi) FROM Odpad o,Katalog_odpadu k WHERE k.id_odpad = o.id_odpad AND  id_zdravotnicke_zarizeni = ? GROUP BY o.id_odpad"
        val = app.usernameL
        data = app.cursor.execute(SQL, val)
        mnozstvi = []
        nazvy = []
        for row in data:
            print(row)
            nazvy.append(row[0])
            mnozstvi.append(row[1])
        plt.figure(1)
        plt.bar(nazvy, mnozstvi, color=(0, 0, 1, 0.6))
        plt.ylabel("Váha (g)")
        plt.xlabel("Kód odpadu")
        self.ids['graf1'].add_widget(FigureCanvasKivyAgg(plt.gcf()))
        plt.figure(2)
        SQL = "SELECT kategorie,SUM(mnozstvi) FROM 	Odpad o,Katalog_odpadu k WHERE k.id_odpad = o.id_odpad AND  id_zdravotnicke_zarizeni = ? GROUP BY kategorie"
        data2 = app.cursor.execute(SQL, val)
        bezpecnost = []
        bezpecnost_name = []
        for row in data2:
            print(row)
            if row[0] == 1:
                bezpecnost.append("Bezpečný")
                bezpecnost_name.append(row[1])
            else:
                bezpecnost.append("Nebezpečný")
                bezpecnost_name.append(row[1])

        bar_bez = plt.bar(bezpecnost, bezpecnost_name)
        bar_bez[0].set_color('r')
        if len(bar_bez) > 1:
            bar_bez[1].set_color('g')

        plt.ylabel("Váha (g)")
        plt.xlabel("Kategorie")
        self.ids['graf2'].add_widget(FigureCanvasKivyAgg(plt.gcf()))

class MainWindow(Screen):

    def on_enter(self, *args):
        self.ids['main_day_of_week'].text = 'Dnes je ' + datetime.today().strftime('%A') + ' ' + date.today().strftime(
            "%d. %m. %Y")
        app = MDApp.get_running_app()
        SQL = "SELECT distinct(datum_uskladneni) FROM Odpad O, Katalog_odpadu K WHERE O.id_odpad = K.id_odpad AND kategorie = 1 AND datum_odvozu IS NULL AND id_zdravotnicke_zarizeni = (?)"
        val = app.usernameL
        data = app.cursor.execute(SQL, val)
        list_of_char = [' ','(',')', '\'',',']
        for row in data:
            x = str(row)
            for char in list_of_char:
                x = x.replace(char,'')
            x = x.split(".")
            date_dbs = date(int(x[2]),int(x[1]),int(x[0]))
            today = date.today()
            days = abs(today - date_dbs).days
            if days//7 >= 1:
                self.dialog = MDDialog(
                    title="Máte uskladněný nebezpečný materiál déle než týden",
                    text="Doporučujeme ho co nejdříve odeslat",
                    radius=[20, 20, 20, 20],
                    size_hint=[.5, .6],
                )
                self.dialog.open()

class Popup_psswd(BoxLayout):
    pass

class Popup_user(BoxLayout):
    pass

class ProfileWindow(Screen):

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        SQL = "SELECT * FROM Zdravotnicke_zarizeni WHERE ico = ? "
        val = app.usernameL
        data = app.cursor.execute(SQL, val)
        for row in data:
            udaje = row
        self.ids['nazev_organizace'].text = udaje[1]
        self.ids['adresa'].text = udaje[2]
        self.ids['ico'].text = udaje[3]
        self.ids['telefon'].text = udaje[4]

        sql = 'Select kategorie,SUM(mnozstvi) from Odpad,Katalog_odpadu WHERE katalogove_cislo = kod_odpadu AND zdravotnicke_zarizeni_ico = ? ' \
              'GROUP BY kategorie'
        val = app.usernameL
        data = app.cursor.execute(sql, val)
        hint_data = []
        for row in data:
            hint_data.append(row)

        if hint_data[0][0] == 0:
            self.ids['progress_bar_bezpecne'].set_value(hint_data[0][1])
            self.ids['progress_bar_nebezpecne'].set_value(hint_data[1][1])
        else:
            self.ids['progress_bar_nebezpecne'].set_value(hint_data[0][1])
            self.ids['progress_bar_bezpecne'].set_value(hint_data[1][1])

    def generateISPOP(self):
        app = MDApp.get_running_app()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=22)
        home = str(Path.home())
        pdf.image("obrazky/logo_plus.png", x=20, y=20,w=60,h=60)
        pdf.cell(200, 30, txt="Zpráva pro ISPOP",ln=1, align='C')
        today = date.today().strftime("-%m-%Y")
        pdf.output(home + "/Desktop/ISPOP" + today + ".pdf");
        Snackbar(
            text="ISPOP zpráva byla úspěšně uložena na plochu",
            snackbar_x="10dp",
            snackbar_y="10dp",
            bg_color=(0, 0, 0, .2)
        ).open()

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

        reg_validity = 1
        # jmeno
        if self.ids['reg_name'].text == "":
            self.ids['reg_error_name'].text = "* Povinné pole"
            reg_validity = 0
        # ico
        if self.ids['reg_ico'].text == "":
            self.ids['reg_error_ico'].text = "* Povinné pole"
            reg_validity = 0
        # elif reg_ico_validity(self.ids['reg_ico'].text) != 1:
        #    self.ids['reg_error_ico'].text = "* Nevalidni ICO"
        #    reg_validity = False
        # adresa
        if self.ids['reg_address'].text == "":
            self.ids['reg_error_address'].text = "* Povinné pole"
            reg_validity = 0
        # telefoni cislo
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
        # heslo
        if self.ids['reg_password'].text == "":
            self.ids['reg_error_password'].text = "* Povinné pole"
            reg_validity = 0
        # heslo2
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

    def reg_to_dbs(self):
        app = MDApp.get_running_app()
        sql = "INSERT INTO Zdravotnicke_zarizeni (heslo, nazev, mesto, ico, telefon) VALUES (?, ?, ?, ?, ?)"
        val = (self.ids['reg_password'].text,
               self.ids['reg_name'].text,
               self.ids['reg_address'].text,
               self.ids['reg_ico'].text,
               self.ids['reg_number'].text
               )

        app.cursor.execute(sql, val)
        app.cursor.commit()

class AddTrashWindow(Screen):

    def choosenTrash(self,n):
        app = MDApp.get_running_app()
        self.ids['vybrany_odpad'].text = n[0]
        app.vybrany_odpad = n[1]
        self.ids['Add_error_mess_Trash'].text = ""

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        self.ids['vybrany_odpad'].text = ""
        self.ids['Add_trash_pole_mnozstvi'].text = "0"
        app.cursor.execute('SELECT * FROM Katalog_odpadu')
        for row in app.cursor:
            widget = TwoLineListItem(text=f"{row[0]}", secondary_text=f"{row[1]}", on_release = lambda x,n=row: self.choosenTrash(n))
            self.ids['container'].add_widget(widget)
            #self.ids['container'].add_widget(TwoLineListItem(text=f"{row[0]}", secondary_text=f"{row[1]}"))

    def trash_change_spinner_icon(self):
        if self.ids['spinner_icon'].icon == 'menu-down':
            self.ids['spinner_icon'].icon = 'menu-up'
        else:
            self.ids['spinner_icon'].icon = 'menu-down'

    def trash_successfulAdd(self):
        app = MDApp.get_running_app()
        valid = True
        if self.ids['vybrany_odpad'].text == "":
            self.ids['Add_error_mess_Trash'].text = "* Povinné pole"
            valid = False
        if self.ids['Add_trash_pole_mnozstvi'].text == "0":
            self.ids['Add_error_mess_Vaha'].text = "* Povinné pole"
            valid = False
        elif self.ids['Add_trash_pole_mnozstvi'].text == "":
            self.ids['Add_error_mess_Vaha'].text = "* Povinné pole"
            valid = False
        elif not self.ids['Add_trash_pole_mnozstvi'].text.isnumeric():
            self.ids['Add_error_mess_Vaha'].text = "* Nečíselná hodnota"
            valid = False
        if valid:
            self.ids['Add_error_mess_Vaha'].text = ""
            if self.ids['drop_item'].text == "kg":
                mnozstvi = float(self.ids['Add_trash_pole_mnozstvi'].text) * 1000
            elif self.ids['drop_item'].text == "dg":
                mnozstvi = float(self.ids['Add_trash_pole_mnozstvi'].text) * 100
            else:
                mnozstvi = float(self.ids['Add_trash_pole_mnozstvi'].text)

            SQL = ('SELECT COUNT(*) FROM Odpad WHERE id_zdravotnicke_zarizeni = (?)')
            val = (app.usernameL)
            pocet = app.cursor.execute(SQL, val)

            if pocet.fetchone()[0] == 0:
                id_odpadu = 1
            else:
                SQL = ('SELECT max(id) FROM Odpad WHERE id_zdravotnicke_zarizeni = (?)')
                val = (app.usernameL)
                nacteny = app.cursor.execute(SQL, val)
                id_odpadu = nacteny.fetchone()[0] + 1

            SQL = ('INSERT INTO Odpad (id, mnozstvi, datum_uskladneni, id_odpad,id_zdravotnicke_zarizeni,ispop) VALUES (?,?,?,?,?,?)')
            val = (id_odpadu, int(mnozstvi),date.today().strftime("%d. %m. %Y"), app.vybrany_odpad,app.usernameL,0)
            app.cursor.execute(SQL,val)
            app.cursor.commit()
            Snackbar(
                text="Úspěšně vloženo",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=(0, 0, 0, .2)
            ).open()

    def on_leave(self, *args):
        self.ids.container.clear_widgets()

class WindowManager(ScreenManager):
    pass

class MeditrashApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__()
        try:
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + '147.230.21.34' + ';DATABASE=' + 'DBS2021_JanPodavka'
                + ';UID=' + 'student' + ';PWD=' + 'student')
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print("Nelze připojit k databázi\n")
            print(sqlstate)
            exit()

        self.cursor = connection.cursor()

    def build(self):
        vybrany_odpad = StringProperty(None)
        usernameL = StringProperty(None)
        passwordL = StringProperty(None)
        selected_rows = "empty"
        instance_data = ObjectProperty(None)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        screen = Builder.load_file("styly.kv")
        return screen

    data = {
        "Změnit heslo": "lock-reset",
        "Upravit profil": "account-edit-outline",
        "Odhlásit se": "logout-variant",
    }
    def callback_update_profile(self, instance):
        if instance.icon == "lock-reset": ##změna hesla
            self.dialog = MDDialog(
                title="Změnit heslo",
                radius=[20, 20, 20, 20],
                size_hint=[.5, .6],
                type="custom",
                auto_dismiss=False,
                content_cls=Popup_psswd(),
                buttons=[
                    MDFlatButton(
                        text="Zpět",
                        on_release= self.close_dialog
                    ),
                    MDFlatButton(
                        text="Uložit",
                        on_release=self.update_psswd
                    ),
                ],
            )
            self.dialog.open()

        elif instance.icon == "account-edit-outline": ##editace účtu
            self.dialog = MDDialog(
                title="Upravit profil",
                radius=[20, 20, 20, 20],
                size_hint=[.5, .8],
                type="custom",
                auto_dismiss=False,
                content_cls=Popup_user(),
                buttons=[
                    MDFlatButton(
                        text="Zpět",
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Uložit",
                        on_release=self.update_user
                    ),
                ],
            )
            self.dialog.open()
        else:
            self.root.current = "login"
            #self.current = "login"

    def close_dialog(self,obj):
         self.dialog.dismiss()
    def update_psswd(self, *args):
        app = MDApp.get_running_app()
        valid = True

        stare_heslo = app.get_data(0)
        if self.dialog.content_cls.ids.profile_old_psswd.text != stare_heslo:
            self.dialog.content_cls.ids.profile_old_psswd.error = True
            self.dialog.content_cls.ids.profile_old_psswd.helper_text = "Chybné heslo"
            valid = False
        if self.dialog.content_cls.ids.profile_new_psswd.text == "":
            self.dialog.content_cls.ids.profile_new_psswd.error = True
            self.dialog.content_cls.ids.profile_new_psswd.helper_text = "Povinné pole"
            valid = False
        if self.dialog.content_cls.ids.profile_new_psswd_check.text == "":
            self.dialog.content_cls.ids.profile_new_psswd_check.error = True
            self.dialog.content_cls.ids.profile_new_psswd_check.helper_text = "Povinné pole"
            valid = False
        elif self.dialog.content_cls.ids.profile_new_psswd.text != self.dialog.content_cls.ids.profile_new_psswd_check.text:
            self.dialog.content_cls.ids.profile_new_psswd.error = True
            self.dialog.content_cls.ids.profile_new_psswd.helper_text = "Hesla se neshodují"
            valid = False

        if valid:
            sql = "UPDATE Zdravotnicke_zarizeni SET heslo = (?) WHERE ico = ? "
            val = (self.dialog.content_cls.ids.profile_new_psswd.text,app.usernameL)
            app.cursor.execute(sql, val)
            app.cursor.commit()
            self.dialog.dismiss(force=True)
            Snackbar(
                text="Heslo úspěšně změněno",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=(0, 0, 0, .2)
            ).open()

    def update_user(self, *args):
        app = MDApp.get_running_app()
        valid = True
        if self.dialog.content_cls.ids.profile_name.text == "":
            self.dialog.content_cls.ids.profile_name.helper_text = "Povinné pole"
            self.dialog.content_cls.ids.profile_name.error = True
            valid = False
        else:
            self.dialog.content_cls.ids.profile_name.error = False

        if self.dialog.content_cls.ids.profile_phone.text == "":
            self.dialog.content_cls.ids.profile_phone.error = True
            self.dialog.content_cls.ids.profile_phone.helper_text = "Povinné pole"
            valid = False
        elif len(self.dialog.content_cls.ids.profile_phone.text) !=9:
            self.dialog.content_cls.ids.profile_phone.error = True
            self.dialog.content_cls.ids.profile_phone.helper_text = "Nesprávné telefoní číslo"
            valid = False
        else:
            self.dialog.content_cls.ids.profile_phone.error = False

        if self.dialog.content_cls.ids.profile_address.text == "":
            self.dialog.content_cls.ids.profile_addres.error = True
            self.dialog.content_cls.ids.profile_addres.helper_text = "Povinné pole"
            valid = False
        else:
            self.dialog.content_cls.ids.profile_address.error = False

        if valid:
            sql = "UPDATE Zdravotnicke_zarizeni SET nazev = (?), mesto = (?), telefon = (?)  WHERE ico = (?)"
            name = self.dialog.content_cls.ids.profile_name.text
            address = self.dialog.content_cls.ids.profile_address.text
            phone = self.dialog.content_cls.ids.profile_phone.text
            val = (name, address, phone, app.usernameL)
            app.cursor.execute(sql, val)
            app.cursor.commit()
            self.dialog.dismiss(force=True)
            print("True")
            self.root.get_screen('profile').ids['telefon'].text = phone
            self.root.get_screen('profile').ids['nazev_organizace'].text = name
            self.root.get_screen('profile').ids['adresa'].text = address

            Snackbar(
                text="Informace úspěšně změněny",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=(0, 0, 0, .2)
            ).open()


    def get_data(self,n):
        app = MDApp.get_running_app()
        SQL = "SELECT * FROM Zdravotnicke_zarizeni WHERE ico = ? "
        val = app.usernameL
        data = app.cursor.execute(SQL, val)
        for row in data:
            udaje = row

        return udaje[n]

if __name__ == '__main__':
    MeditrashApp().run()







