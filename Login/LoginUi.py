import sys
import os
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QFrame, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QMessageBox, QApplication
)

try:
    from . import constants as cn
    from . import functions as fn
except ImportError:
    import constants as cn
    import functions as fn


class Login(QWidget):
    switch_window = QtCore.pyqtSignal(list, str)
    switch_window_user = QtCore.pyqtSignal(tuple)
    # switch_window_aduana = QtCore.pyqtSignal(str)

    def __init__(self, path, database):
        super().__init__()
        self.root_path = path
        self.database = database

        self.setWindowIcon(QIcon(f'{self.root_path}/src/SioV2.ico'))
        self.setWindowTitle('Login')
        self.setFixedSize(600, 450)

        self.setStyleSheet('background-color: #9c9c9c;')

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setStyleSheet(cn.tab_style)

        layout.addWidget(self.tab_widget)

#########################################################################
#########################################################################

        self.tab1 = QFrame()
        tab1_layout = QGridLayout()
        self.tab1.setLayout(tab1_layout)
        self.tab1.setStyleSheet('background-color: #fff;')

        self.label_user = QLabel()
        self.label_user.setText('Num. de Reloj')

        self.label_password = QLabel()
        self.label_password.setText('Contraseña')

        self.line_user = QLineEdit()
        self.line_user.setAlignment(QtCore.Qt.AlignCenter)

        self.line_password = QLineEdit()
        self.line_password.setAlignment(QtCore.Qt.AlignCenter)
        self.line_password.setEchoMode(QLineEdit.Password)

        self.logo = QPixmap(f'{self.root_path}/src/logo-rojo-v2.png')
        self.label_logo = QLabel()
        self.label_logo.setMaximumWidth(200)
        self.label_logo.setPixmap(self.logo)
        self.label_logo.setScaledContents(True)

        tab1_layout.addWidget(self.label_logo, 1, 2, 2, 2)

        tab1_layout.addWidget(self.label_user, 3, 2, 1, 2)
        tab1_layout.addWidget(self.line_user, 4, 2, 1, 2)

        tab1_layout.addWidget(self.label_password, 6, 2, 1, 2)
        tab1_layout.addWidget(self.line_password, 7, 2, 1, 2)

        self.spacer1 = QSpacerItem(
            30, 30, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacer_c = QSpacerItem(
            55, 30, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.spacer_r = QSpacerItem(
            30, 50, QSizePolicy.Expanding, QSizePolicy.Fixed)

        tab1_layout.addItem(self.spacer_c, 0, 0)
        tab1_layout.addItem(self.spacer_r, 0, 1)
        tab1_layout.addItem(self.spacer_r, 0, 2)
        tab1_layout.addItem(self.spacer_r, 0, 3)
        tab1_layout.addItem(self.spacer_r, 0, 4)
        tab1_layout.addItem(self.spacer_c, 0, 5)

        tab1_layout.addItem(self.spacer_r, 2, 1)
        tab1_layout.addItem(self.spacer_r, 5, 1)
        tab1_layout.addItem(self.spacer_r, 8, 1)


#########################################################################
#########################################################################

        self.tab2 = QFrame()
        self.tab2.setObjectName("tab2")

        tab2_layout = QGridLayout()
        self.tab2.setLayout(tab2_layout)

        self.tab2.setStyleSheet(f'''
            QFrame {{
                background-image: url({self.root_path}/src/blue.jpg);
                background-repeat: no-repeat;
                background-position: center;
            }}

        ''')

        self.inv_code = QLineEdit()
        self.inv_code.setAlignment(QtCore.Qt.AlignCenter)
        self.inv_code.setEchoMode(QLineEdit.Password)
        self.inv_code.setStyleSheet(cn.line_style)

        self.logo2 = QPixmap(f'{self.root_path}/src/logo-rojo-v2.png')
        self.label_logo2 = QLabel()
        self.label_logo2.setMaximumWidth(200)
        self.label_logo2.setMaximumHeight(170)
        self.label_logo2.setPixmap(self.logo)
        self.label_logo2.setScaledContents(True)
        self.label_logo2.setStyleSheet('''border-image: none;
            background: none;
            padding-left: 15px;
            ''')

        tab2_layout.addWidget(self.label_logo2, 1, 2, 2, 2)

        tab2_layout.addWidget(self.inv_code, 4, 2, 1, 2)

        tab2_layout.addItem(self.spacer_c, 0, 0)
        tab2_layout.addItem(self.spacer_r, 0, 1)
        tab2_layout.addItem(self.spacer_r, 0, 2)
        tab2_layout.addItem(self.spacer_r, 0, 3)
        tab2_layout.addItem(self.spacer_r, 0, 4)
        tab2_layout.addItem(self.spacer_c, 0, 5)

        tab2_layout.addItem(self.spacer_r, 4, 1)
        tab2_layout.addItem(self.spacer_r, 3, 1)
        tab2_layout.addItem(self.spacer_r, 5, 1)


#########################################################################
#########################################################################

        self.tab_widget.addTab(self.tab1, 'Usuario')
        self.tab_widget.addTab(self.tab2, 'Inventario')


#########################################################################
#########################################################################

        self.error = QMessageBox()
        self.error.setWindowTitle('Error')
        self.error.setIcon(QMessageBox.Critical)

        self.warning = QMessageBox()
        self.warning.setWindowTitle('Advertencia')
        self.warning.setText('No Se A Detectado Ninguna Bascula')
        self.warning.setIcon(QMessageBox.Warning)

        self.noConection = QMessageBox()
        self.noConection.setWindowTitle('Error')
        self.noConection.setText(
            'No Se Pudo Establecer La Conexcion Con El Servidor!')
        self.noConection.setIcon(QMessageBox.Critical)


#########################################################################
#########################################################################

        self.inv_code.returnPressed.connect(self.login_inv)
        self.line_user.returnPressed.connect(self.sel_pass)
        self.line_password.returnPressed.connect(self.login_user)
        self.tab_widget.currentChanged.connect(self.set_cursor)

        self.line_user.setFocus()

#########################################################################
#########################################################################

    def sel_pass(self):
        self.line_password.setFocus()

    def set_cursor(self):
        index = self.tab_widget.currentIndex()
        if index == 0:
            self.line_user.setFocus()
        else:
            self.inv_code.setFocus()

    def login_inv(self):
        query = self.inv_code.text().strip()
        area = fn.get_inv_area(query, self.database)
        unconected = "No Conection"
        if area and area != unconected:
            port = fn.set_port()
            if not port:
                port = '0'
            if port == '0':
                self.warning.exec_()
            self.switch_window.emit(area[2:], port)
        elif area == unconected:
            self.noConection.exec_()
            self.inv_code.setText('')
        else:
            self.error.setText('Codigo Incorrecto')
            self.error.exec_()
            self.inv_code.setText('')

    def login_user(self):
        query = self.line_user.text().strip()
        passwd = self.line_password.text().strip()
        user = fn.search_user(query, self.database)
        unconected = "No Conection"
        if user and user != unconected:
            if query == str(user[0]) and passwd == user[1]:
                self.switch_window_user.emit(user)
            else:
                self.error.setText('Constraseña Incorrecta')
                self.error.exec_()
        elif user == unconected:
            self.noConection.exec_()
            self.line_user.setText('')
        else:
            self.error.setText('Usuario No Encontrado')
            self.error.exec_()
            self.line_user.setText('')

    def login(self):
        query = self.line_1.text().strip()
        area = fn.get_inv_area(query, self.database)
        user = fn.search_user(query, self.database)
        unconected = "No Conection"

        if area and area != unconected:
            port = fn.set_port()
            if not port:
                port = '0'
            if port == '0':
                self.warning.exec_()
            self.switch_window.emit(area[2], area[3], area[4], area[5], port)
        elif query in cn.aduana_areas and (
                user != unconected or area != unconected):
            self.switch_window_aduana.emit(cn.aduana_areas[query][1])
        elif user and user != unconected:
            if query == str(user[0]):
                self.switch_window_user.emit(
                    user[0], user[1], user[2], user[3], user[4], user[5])
        elif user == unconected or area == unconected:
            self.noConection.exec_()
            self.line_1.setText('')

        else:
            self.error.exec_()
            self.line_1.setText('')


def main():
    app = QApplication(sys.argv)

    window = Login('/'.join(os.getcwd().split('\\'))[:-5], cn.db)
    window.setStyleSheet('background-color: #fff;')
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
