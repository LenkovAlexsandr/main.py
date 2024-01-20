from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QInputDialog
import sqlite3


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 150, 600, 800)
        self.setWindowTitle('Меню')
        self.setMinimumSize(600, 800)
        self.setMaximumSize(600, 800)
        # Создание таблицы блюд
        self.table = QTableWidget(0, 1, self)
        self.table.resize(550, 700)
        self.table.setHorizontalHeaderLabels(['Наименование                    Вес                    Цена'])
        con = sqlite3.connect('database.db')
        cur = con.cursor()  # Запрос в базу данных
        self.data = cur.execute("""SELECT * FROM list_of_dishes""").fetchall()
        self.table.setRowCount(len(self.data))
        for i, val in enumerate(self.data):
            self.table.setItem(i, 0, QTableWidgetItem('\t'.join(val)))
        self.table.resizeColumnsToContents()
        # Кнопка выхода
        self.btn_exit = QPushButton('Выход', self)
        self.btn_exit.resize(50, 25)
        self.btn_exit.move(550, 0)
        self.btn_exit.clicked.connect(self.close)
        # Кнопка заказа
        self.btn_order = QPushButton('Заказать', self)
        self.btn_order.move(230, 720)
        self.btn_order.resize(120, 40)
        self.btn_order.clicked.connect(self.order)
        # Пояснение
        self.label = QLabel('Выберите нужный пункт', self)
        self.label.move(10, 705)

    def order(self):  # Вызов окна с подвержением заказа
        tmp, ok_pressed = QInputDialog.getInt(self, "Подвержение", "Выберите количество", 1, 1, 20, 1)
        if ok_pressed:  # Занесение заказа в таблицу, если подтвердили заказ
            try:
                product = self.data[self.table.selectedItems()[0].row()]
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                if cur.execute(f"SELECT * FROM orders WHERE name = '{product[0]}'").fetchall():
                    # Если уже заказывали этот товар, то увеличиваем количество
                    cur.execute(f"UPDATE orders SET count = count+{tmp} WHERE name = '{product[0]}'")
                else:  # Если такого ещё не заказывали
                    cur.execute(f"INSERT INTO orders(name,count) VALUES('{product[0]}', '{tmp}')")
                con.commit()
            except Exception:
                pass
