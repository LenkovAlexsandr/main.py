from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QInputDialog
import sqlite3


class Orders(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Запрос в базу данных заказов
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        self.data_orders = cur.execute("""SELECT * FROM orders""").fetchall()
        if self.data_orders:  # Если, что-то заказали
            self.setGeometry(700, 150, 600, 800)
            self.setWindowTitle('Заказ')
            self.setMinimumSize(600, 800)
            self.setMaximumSize(600, 800)
            # Создание тоблицы с заказом
            self.table = QTableWidget(0, 1, self)
            self.table.resize(500, 700)
            self.table.setHorizontalHeaderLabels(['Наименование          Количество          Стоймость'])
            self.table.setRowCount(len(self.data_orders))
            total_cost = 0
            for i, val in enumerate(self.data_orders):  # Заполнение таблицы
                name, quantity = val
                cost = int(quantity) * int(cur.execute(f"SELECT * FROM list_of_dishes WHERE name = '{name}'").
                                           fetchall()[0][2].split()[0])
                total_cost += cost
                self.table.setItem(i, 0, QTableWidgetItem(name + '\t' + str(quantity) + '\t' + str(cost)))
            self.table.resizeColumnsToContents()
            # Вывод общей стоймости
            self.label_cost = QLabel('Всего к оплате: ' + str(total_cost), self)
            self.label_cost.move(390, 720)
            # Кнопка выхода
            self.btn_exit = QPushButton('Выход', self)
            self.btn_exit.resize(100, 25)
            self.btn_exit.move(500, 0)
            self.btn_exit.clicked.connect(self.close)
            # кнопка полной очистки заказа
            self.btn_del_all = QPushButton('Удалить заказа', self)
            self.btn_del_all.resize(100, 25)
            self.btn_del_all.move(500, 60)
            self.btn_del_all.clicked.connect(self.delete_all)
            # кнопка удалениу выбранного заказа
            self.btn_del_one = QPushButton('Удалить пункт', self)
            self.btn_del_one.resize(100, 25)
            self.btn_del_one.move(500, 100)
            self.btn_del_one.clicked.connect(self.delete_one)
            # Кнопка для изменения количества заказаного
            self.btn_edit = QPushButton('Изменить\nколичество', self)
            self.btn_edit.resize(100, 35)
            self.btn_edit.move(500, 140)
            self.btn_edit.clicked.connect(self.edit)
            # Кнопка выполнения заказа
            self.btn_perform = QPushButton('Заказать', self)
            self.btn_perform.resize(150, 50)
            self.btn_perform.move(225, 720)
            self.btn_perform.clicked.connect(self.perform)
        else:  # Если заказ пуст
            self.setGeometry(850, 400, 300, 300)
            self.setWindowTitle('Заказ')
            self.setMinimumSize(300, 300)
            self.setMaximumSize(300, 300)
            self.label = QLabel('Вы ещё ничего не заказали.', self)
            self.label.move(80, 40)
            self.btn_exit = QPushButton('Выход', self)
            self.btn_exit.resize(100, 50)
            self.btn_exit.move(100, 150)
            self.btn_exit.clicked.connect(self.close)

    def delete_all(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()  # Очистка базы данных
        cur.execute("""DELETE FROM orders""").fetchall()
        con.commit()
        self.close()  # Закрытие окна

    def delete_one(self):  # Удаление
        try:
            product = self.data_orders[self.table.selectedItems()[0].row()]
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute(f"""DELETE FROM orders WHERE name = '{product[0]}'""").fetchall()
            con.commit()
            self.close()
        except Exception:
            pass

    def edit(self):  # Изменение количества
        try:
            product = self.data_orders[self.table.selectedItems()[0].row()]
            tmp, ok_pressed = QInputDialog.getInt(self, "Подвержение", "Выберите количество", 1, -int(product[1]), 20, 1)
            if ok_pressed:
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                if tmp == -int(product[1]):
                    cur.execute(f"""DELETE FROM orders WHERE name = '{product[0]}'""").fetchall()
                else:
                    cur.execute(f"UPDATE orders SET count = count+{tmp} WHERE name = '{product[0]}'")
                con.commit()
                self.close()
        except Exception:
            pass

    def perform(self):
        # Здесь должна быть передача заказа дальше, но я это не сделал так как
        # я работаю только над графическим интерфейсом
        pass
