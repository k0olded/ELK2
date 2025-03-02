import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.lang import Builder
import sqlite3
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import sqlite3
import hashlib
import datetime

Window.size = (720, 1600)
#Window.clearcolor = (20/255, 20/255, 88/255, 1)
background_normal='bg.jpg'
Window.title = 'elk'
local_data = []
days_of_week = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
class MyNewScreen(BoxLayout):
    #Это мой новый экран
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
hello = []
reg = []
data_of_body = []
main = []
dbn_food = 'food.db'
dbn_users = 'data.db' #для удобства оценки и демонстрации подключаем БД с пользователями ЛОКАЛЬНО
a = 0

class MainScreen(BoxLayout):
    #Главный экран, на котором все будет происходить
    def __init__(self,**kwargs):
        self.num=1
        self.another_num=1
        super().__init__(**kwargs)

    def my_update(self):
        # проходит по списку всех детей виджета под именем another_box
        for child in self.ids.another_box.children:
            child.text = "test update - {}".format(self.another_num * self.num)
            self.another_num += 1



class MyApp(App):
    def cleare_widgets_in_another_box(self):
        for i in range(len(self.ids.another_box.children)):
            self.ids.another_box.remove_widget(self.ids.another_box.children[-1])
    def recreate(self, *args):
        # удаляет все виджеты и создает новые виджеты
        #self.cleare_widgets_in_another_box()
        self.label.opacity = 0
        self.input_data1.opacity = 0
        self.input_data2.opacity = 0
        self.input_data3.opacity = 0
        self.input_data4.opacity = 0
        self.btn_1.opacity = 0

    def create_widgets_in_another_box(self):
        # создает новые виджеты в виджете another_box
        for i in range(5):
            self.ids.another_box.add_widget(
                Label(text="Test create - {}".format(i + self.num), size_hint_y=None, height=100))
    def set_bg(self, *args):
        self.root_window.bind(size=self.do_resize)
        with self.root_window.canvas.before:
            self.bg = Rectangle(source='bg.jpg', pos=(0,0), size=(self.root_window.size))

    def __init__(self):
        global hello, reg, data_of_body, main
        super().__init__()
        #welcome page
        self.label = Label(text='Добро пожаловать!')
        self.hello_lbl = Label(text="Для начала использования приложения пройдите регистрацию или авторизацию!")
        self.btn_reg = Button(text='Регистрация', size_hint_x=0.33, width=100,
                            background_color=(243 / 255, 183 / 255, 48 / 255, 1))  # background_normal='btn_bg.png')
        self.btn_log = Button(text='Вход', size_hint_x=0.33, width=100,
                            background_color=(243 / 255, 183 / 255, 48 / 255, 1))  # background_normal='btn_bg.png')
        self.btn_reg.bind(on_press=self.register)
        self.btn_log.bind(on_press=self.login)

        hello = [self.label, self.hello_lbl, self.btn_reg, self.btn_log]

        #registration
        self.reg_label = Label(text='Регистрация')
        self.input_data1 = TextInput(hint_text='ФИО', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data2 = TextInput(hint_text='Пароль', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data3 = TextInput(hint_text='класс', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data4 = TextInput(hint_text='школа', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.button1 = Button(text="зарегистрироваться", size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .8})
        self.button1.bind(on_press=self.body_data)

        reg = [self.input_data1, self.input_data2, self.input_data3, self.input_data4, self.button1]

        # data_of_body
        self.body_label = Label(text='Ещё немного')
        self.input_data5 = TextInput(hint_text='пол(М/Ж)', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data6 = TextInput(hint_text='вес', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data7 = TextInput(hint_text='рост', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data8 = TextInput(hint_text='возраст', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.button2 = Button(text="Подтвердить", size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .8})
        self.button2.bind(on_press=self.registering)

        data_of_body = [self.input_data1, self.input_data2, self.input_data3, self.input_data4, self.button1]

        #main
        self.main_label = Label(text='Меню')
        self.btn_settings = Button(text="Питание", size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .8})
        self.btn_settings.bind(on_press=self.table)
        self.btn_menu = Button(text="Настройки", size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .8})
        self.btn_menu.bind(on_press=self.table)

        main = [self.main_label, self.btn_settings, self.btn_menu]

        # login
        self.login_label = Label(text='Вход')
        self.input_data9 = TextInput(hint_text='ФИО', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.input_data0 = TextInput(hint_text='Пароль', size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .6})
        self.button3 = Button(text="Вход", size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .8})
        self.button3.bind(on_press=self.logining)

        # table
        self.table_label = Label(text="Ваша дневная норма килокаллорий:")
        self.button_of_table = Button(text="", size_hint_x=0.33, width=100, pos_hint={'x': .4, 'y': .8})

    def login(self, *args):
        global  hello, local_data
        main_layout.clear_widgets()
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.login_label)
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data9)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data0)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.button3)

    def table(self, *args):
        global a
        global local_data
        m = 0
        k = 0
        print(local_data)
        print(local_data[6])
        if local_data[6] == "м":
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            k = local_data[7] + local_data[8] - local_data[9] + 5
            k = int(round(k, 0))
            print(k)
        elif local_data[6] == "ж":
            k = local_data[7] + local_data[8] - local_data[9] - 161
            k = int(round(k, 0))
        self.table_label.text = f"Ваша дневная норма килокаллорий: {k}."
        conn = sqlite3.connect(dbn_food)
        cursor = conn.cursor()
        quest = f"""SELECT * FROM lunch"""
        cursor.execute(quest)
        datas = cursor.fetchall()
        conn.commit()
        conn.close()
        print(datas)
        main_layout.clear_widgets()
        n_layout = GridLayout(cols=9, rows=9, padding=[80], size_hint=[1, 1])
        n_layout.add_widget(Label(text=''))
        n_layout.add_widget(Label(text=''))
        n_layout.add_widget(Label(text='ваше меню на'))
        n_layout.add_widget(Label(text=''))
        n_layout.add_widget(Label(text=''))
        n_layout.add_widget(Label(text='ПОНЕДЕЛЬНИК'))
        n_layout.add_widget(Label(text=''))
        n_layout.add_widget(Label(text=''))

        n_layout.add_widget(Button(text=''))
        n_layout.add_widget(Button(text='блюдо'))
        n_layout.add_widget(Button(text=''))
        n_layout.add_widget(Button(text='вес(г)'))
        n_layout.add_widget(Button(text='белки'))
        n_layout.add_widget(Button(text='жиры'))
        n_layout.add_widget(Button(text='углеводы'))
        n_layout.add_widget(Button(text='ккал'))

        for i in datas:
            print(i)
            if datetime.datetime.today().weekday() > 4:
                a == 0
            else:
                a = datetime.datetime.today().weekday()
            if i[0] == days_of_week[a]:
                n_layout.add_widget(Label(text=''))
                n_layout.add_widget(Label(text=i[1]))
                n_layout.add_widget(Label(text=''))
                n_layout.add_widget(Button(text=str(i[2])))
                n_layout.add_widget(Button(text=str(i[3])))
                n_layout.add_widget(Button(text=str(i[4])))
                n_layout.add_widget(Button(text=str(i[5])))
                n_layout.add_widget(Button(text=str(i[6])))
                m += 1
                if m == 4:
                    break
        return n_layout
    def logining(self, *args):
        global local_data
        conn = sqlite3.connect(dbn_users)
        cursor = conn.cursor()
        quest = f"""SELECT * FROM data"""
        cursor.execute(quest)
        datas = cursor.fetchall()
        conn.commit()
        conn.close()
        print(datas)
        flag2 = False
        for i in datas:
            print(f"{i[1]}:{hashlib.md5(self.input_data9.text.encode()).hexdigest()}")
            if i[1] == hashlib.md5(self.input_data9.text.encode()).hexdigest():
                if i[2] == hashlib.md5(self.input_data0.text.encode()).hexdigest():
                    print(f"Succesful! Welcome, {self.input_data9.text}!")
                    flag2 = True
                    local_data = i
                    self.main_menu()
                    break
        if flag2 == False:
            self.input_data0.text = ""
            self.input_data9.text = ""
            return 0

    def register(self, *args):
        global  hello, local_data
        main_layout.clear_widgets()
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.reg_label)
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data1)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data2)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data3)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(self.input_data4)
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.button1)
    def registering(self, *args):
        global main, local_data
        login_hash = self.input_data5.text
        pass_hash = self.input_data6.text
        class_ = self.input_data7.text
        school = self.input_data8.text
        local_data.append(login_hash)
        local_data.append(pass_hash)
        local_data.append(class_.lower())
        local_data.append(school)
        dbc = sqlite3.connect(dbn_users)
        cursor = dbc.cursor()
        request = f"""INSERT INTO data(user, password, login, classs, school, gender, mass, height, ages)VALUES('{local_data[0]}','{local_data[1]}','{local_data[2]}','{local_data[3]}','{local_data[4]}','{local_data[5]}', {local_data[6]}, {local_data[7]}, {local_data[8]})"""
        print(request)
        cursor.execute(request)
        dbc.commit()
        dbc.close()
        self.main_menu()
    def body_data(self, *args):
        global data_of_body, local_data
        login_hash = hashlib.md5(self.input_data1.text.encode()).hexdigest()
        pass_hash = hashlib.md5(self.input_data2.text.encode()).hexdigest()
        class_ = self.input_data3.text
        school = self.input_data4.text
        local_data.append(login_hash)
        local_data.append(pass_hash)
        local_data.append(self.input_data1.text)
        local_data.append(class_)
        local_data.append(school)
        print(local_data)
        main_layout.clear_widgets()
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.body_label)
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data5)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data6)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.input_data7)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(self.input_data8)
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.button2)
    def main_menu(self, *args):

        main_layout.clear_widgets()
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.main_label)
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.btn_menu)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.btn_settings)

    def do_resize(self, *args):
        self.bg.size = self.root_window.size
    def change_input_data1(self, instance):
        self.input_data1.text='пол'

    def change_input_data2(self, instance):
        self.input_data2.text='вес'

    def change_input_data3(self, instance):
        self.input_data3.text='рост'

    def change_input_data4(self, instance):
        self.input_data4.text='возраст'

    def change_label(self, instance):
        self.label.text='ввод параметров'
    def change_btn_1(self, instance):
        self.btn_1.text='составить меню'








    def build(self):
        global main_layout
        # Все объекты будем помещать в один общий слой
        Clock.schedule_once(self.set_bg, 0)
        main_layout = GridLayout(cols=3, rows=26, row_force_default=True, row_default_height=60)
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.label)
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.hello_lbl)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.btn_log)

        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(Label(text=''))
        main_layout.add_widget(self.btn_reg)
        return main_layout




if __name__ == "__main__":
    MyApp().run()
