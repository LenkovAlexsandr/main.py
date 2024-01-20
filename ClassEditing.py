from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
import sqlite3


class Editing(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 200, 600, 600)
        self.setWindowTitle('Редактирование')
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        # Кнопка для закрытия окна
        self.btn_exit = QPushButton('Закрыть', self)
        self.btn_exit.resize(70, 25)
        self.btn_exit.move(530, 0)
        self.btn_exit.clicked.connect(self.close)
        # Изменение пароля
        self.label_new_password = QLabel('Введите новый пароли и нажмите на кнопку "Изменить пароль",'
                                         ' чтобы сохранить новый пароль', self)
        self.label_new_password.move(10, 10)
        # Поле ввода для нового пароля
        self.field_new_password = QLineEdit(self)
        self.field_new_password.move(10, 30)
        self.field_new_password.resize(200, 25)
        # Кнопка для сохранения нового пароля
        self.btn_new_password = QPushButton('Изменить пароль', self)
        self.btn_new_password.resize(100, 25)
        self.btn_new_password.move(250, 30)
        self.btn_new_password.clicked.connect(self.new_password)
        # Добавление нового продукта
        self.label_new_product = QLabel('Заполните все поля и нажмите кнопку "Добавить",'
                                        ' чтобы добавить продукт в меню', self)
        self.label_new_product.move(10, 75)

        # Имя
        self.label_name_of_fields = QLabel('Наименование', self)
        self.label_name_of_fields.move(10, 95)
        self.field_name = QLineEdit(self)
        self.field_name.move(10, 115)
        self.field_name.resize(200, 25)
        # Вес
        self.label_weight_of_fields = QLabel('Вес (в граммах, вводить целочисленное число)', self)
        self.label_weight_of_fields.move(10, 150)
        self.field_weight = QLineEdit(self)
        self.field_weight.move(10, 170)
        self.field_weight.resize(200, 25)
        # Цена
        self.label_price_of_fields = QLabel('Цена(в руб, вводить целочисленное число)', self)
        self.label_price_of_fields.move(10, 205)
        self.field_price = QLineEdit(self)
        self.field_price.move(10, 225)
        self.field_price.resize(200, 25)
        # Кнопка добавления продукта
        self.btn_new_product = QPushButton('Добавить', self)
        self.btn_new_product.resize(150, 50)
        self.btn_new_product.move(300, 120)
        self.btn_new_product.clicked.connect(self.new_product)
        # Вывод при дабовлении нового продукта
        self.label_output = QLabel('', self)
        self.label_output.move(300, 200)
        # Удаление
        self.label_delete = QLabel('Введите наименование позиции которую хотите удалить и нажимайте кнопку "Удалить"',
                                   self)
        self.label_delete.move(10, 280)
        self.field_delete = QLineEdit(self)
        self.field_delete.resize(200, 25)
        self.field_delete.move(10, 300)
        # Кнопка Удаление пункта
        self.btn_delete = QPushButton('Удалить', self)
        self.btn_delete.resize(150, 40)
        self.btn_delete.move(300, 315)
        self.btn_delete.clicked.connect(self.delete)
        # Вывод про удаление пункта
        self.label_delete_output = QLabel(self)
        self.label_delete_output.move(10, 330)
        # Обмен позициями
        self.label_swap = QLabel('Введите два номера позиций которые хотите поменять местами', self)
        self.label_swap.move(10, 380)
        self.field_swap_1 = QLineEdit(self)
        self.field_swap_1.resize(50, 25)
        self.field_swap_1.move(10, 400)
        self.field_swap_2 = QLineEdit(self)
        self.field_swap_2.resize(50, 25)
        self.field_swap_2.move(75, 400)
        self.label_swap_output = QLabel(self)
        self.label_swap_output.move(10, 435)
        # Кнопка обмен позициями
        self.btn_swap = QPushButton('Обмен', self)
        self.btn_swap.resize(150, 40)
        self.btn_swap.move(300, 400)
        self.btn_swap.clicked.connect(self.swap)

    def new_password(self):  # Заменяет пароль
        with open('password.txt', 'w+') as file:
            file.truncate()
            file.write(self.field_new_password.text())

    def new_product(self):
        name = self.field_name.text()
        weight = self.field_weight.text()
        price = self.field_price.text()
        if name and weight and price:  # Если поля заполнены
            try:
                int(weight)  # Проверка коректности ввода
                int(price)
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                if cur.execute(f"SELECT * FROM list_of_dishes WHERE name = '{name}'"):  # При совпадении имени
                    cur.execute(f"DELETE FROM list_of_dishes WHERE name = '{name}'")  # Удаляем старую запись
                    con.commit()
                cur.execute(f"INSERT INTO list_of_dishes(name, weight, price) VALUES('{name}', "
                            f"'{weight} гр.', '{price} руб.')")
                con.commit()
                self.label_output.setText('Продукт добавлен')
                self.label_output.adjustSize()
            except ValueError:  # Если не вверный ввод
                self.label_output.setText('Не корректный ввод')
                self.label_output.adjustSize()
        else:  # Если не все поля заполнены
            self.label_output.setText('Не все поля заполнены!')
            self.label_output.adjustSize()

    def delete(self):  # Удаляет пункт
        name = self.field_delete.text()
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        if cur.execute(f"SELECT * FROM list_of_dishes WHERE name = '{name}'").fetchall():  # Проверка на наличие
            cur.execute(f"DELETE FROM orders WHERE name = '{name}'")
            cur.execute(f"DELETE FROM list_of_dishes WHERE name = '{name}'")
            con.commit()
            self.label_delete_output.setText('Товар удален')
            self.label_delete_output.adjustSize()
        else:  # Если такого имени нету
            self.label_delete_output.setText('Товара с таким наименование нету')
            self.label_delete_output.adjustSize()

    def swap(self):  # Выполняет обмен позиций местами
        a = self.field_swap_1.text()
        b = self.field_swap_2.text()
        if a and b:  # Проверка на заполнение
            try:
                a = int(a) - 1
                b = int(b) - 1
                assert a >= 0 and b >= 0  # Номер позиции должен быть больше нуля
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                data = cur.execute('SELECT * FROM list_of_dishes').fetchall()
                assert a < len(data) and b < len(data)
                data[a], data[b] = data[b], data[a]
                cur.execute('DELETE FROM list_of_dishes')
                for name, weight, price in data:
                    cur.execute(f"INSERT INTO list_of_dishes(name, weight, price) VALUES('{name}', "
                                f"'{weight.split()[0]} гр.', '{price.split()[0]} руб.')")
                con.commit()
                self.label_swap_output.setText('Обмен выполнен')
                self.label_swap_output.adjustSize()
            except Exception:  # Если ошибка в веденных номерах позиций
                self.label_swap_output.setText('Не коректно введены номера позиции(ий)')
                self.label_swap_output.adjustSize()
        else:  # Если поле(я) не заполнено(ы)
            self.label_swap_output.setText('Введены не все позиции')
            self.label_swap_output.adjustSize()
