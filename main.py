import sys
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QInputDialog
from ClassMenu import Menu
from ClassOrders import Orders
from ClassEditing import Editing


class Menu_base(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создание начального окна
        self.setGeometry(800, 200, 400, 600)
        self.setWindowTitle('Меню')
        self.setMinimumSize(400, 600)
        self.setMaximumSize(400, 600)
        # Размещаю картинку
        self.label = QLabel(self)
        self.movie = QMovie("menu1.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
        # Кнопка открытия окна меню
        self.btn_menu = QPushButton('Меню', self)
        self.btn_menu.resize(150, 60)
        self.btn_menu.move(125, 300)
        self.btn_menu.clicked.connect(self.start_menu)
        # Кнопка открытия окна заказов
        self.btn_cart = QPushButton('Заказы', self)
        self.btn_cart.resize(150, 60)
        self.btn_cart.move(125, 400)
        self.btn_cart.clicked.connect(self.start_cart)
        # Кнопка закрытия окна
        self.btn_exit = QPushButton('Выход', self)
        self.btn_exit.resize(150, 60)
        self.btn_exit.move(125, 500)
        self.btn_exit.clicked.connect(self.close)
        # Кнопка для окрытия окна редактора меню
        self.btn_editing = QPushButton(self)
        self.btn_editing.resize(15, 15)
        self.btn_editing.move(386, 586)
        self.btn_editing.clicked.connect(self.editing)

    def start_menu(self):
        # Запуск окна с меню
        self.menu = Menu()
        self.menu.show()

    def start_cart(self):
        # Запуск окна с заказами
        self.cart = Orders()
        self.cart.show()

    def editing(self):
        # Проверка пароля
        password, ok_pressed = QInputDialog.getText(self, "Проверка", "Введите пароль.")
        with open('password.txt', 'r') as file:
            Password = file.readline()
        if ok_pressed and Password == password:  # При верном ответе открывает окно редактирования
            self.editing = Editing()
            self.editing.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windos = Menu_base()
    windos.show()
    sys.exit(app.exec())
