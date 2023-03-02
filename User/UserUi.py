import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import date
import os
from .Passwd import PasswdUi
from .Rivian import RivianUi
from .Aduana import AduanaUi

class User(QMainWindow):

    def __init__(self, user, path, database, close_callback=False):
        super().__init__()

        self.noreloj = user[0]
        self.passwd = user[1]
        self.nombre_completo = user[2]
        self.area = user[3]
        self.subarea = user[4]
        self.turno = user[5]
        self.acceso = [ i.strip() for i in user[6].split(',') ]
        self.path = path
        self.database = database
        self.today = [ int(i) for i in str(date.today()).split('-') ]
        self.close_callback = close_callback

        self.pass_wd = None
        self.rivian_ui = None
        self.aduan_ui = None

        self.setWindowTitle("Usuario")
        self.setFixedSize(QtCore.QSize(220, 350))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

        menuBar = QMenuBar()

        fileMenu = QMenu("&File", self)
        self.button_salir = QAction("&Salir", self)
        self.button_salir.setStatusTip("Salir")
        self.button_passwd = QAction("&Passwd", self)
        self.button_passwd.setStatusTip("Passwd")

        fileMenu.addAction(self.button_passwd)
        fileMenu.addAction(self.button_salir)

        op_menu = QMenu("&Herramientas", self)
        self.button_baño = QAction("&Permisos")
        op_menu.addAction(self.button_baño)

        fe_menu = QMenu("&Feeder", self)
        self.button_aduana = QAction("&Aduana")
        self.button_rivian = QAction("&Rivian")
        fe_menu.addAction(self.button_aduana)
        fe_menu.addAction(self.button_rivian)

        ad_menu = QMenu("&Admin", self)
        self.button_usuarios = QAction("&Usuarios")
        ad_menu.addAction(self.button_usuarios)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(op_menu)
        menuBar.addMenu(fe_menu)
        menuBar.addMenu(ad_menu)

        self.setMenuBar(menuBar)

        main_widget = QWidget(self)
        main_widget.setStyleSheet('''
            background-color: black;
        ''')
        self.setCentralWidget(main_widget)

        main_grid = QGridLayout()
        main_widget.setLayout(main_grid)

        # user_image = f'{self.path}/src/fotos/{self.noreloj}.png'
        user_image = f'//172.18.0.45/Engineering/0. Backup Ingenieria 27/Elaboracion/SIO/fotos/{self.noreloj}.PNG'
        default_image = f'{self.path}/src/default.png'

        self.user = QPixmap(user_image if os.path.exists(user_image) else default_image)
        self.label_img = QLabel()
        self.label_img.setPixmap(self.user)
        self.label_img.setScaledContents(True)
        self.label_img.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
        self.label_img.setStyleSheet('''
            border-style: solid;
            border-color: black;
            border-width: 3px;
            ''')

        labelFont = QFont(QFont('Consolas', 10))
        labelFont.setBold(True)
        self.label_name = QLabel()
        self.label_name.setStyleSheet('''
            background-color: white;
        ''')
        self.label_name.setText(self.nombre_completo)
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setFont(labelFont)

        self.label_id = QLabel()
        self.label_id.setStyleSheet('''
            background-color: white;
        ''')
        self.label_id.setText(str(f'{self.noreloj} : {self.subarea}'))
        self.label_id.setAlignment(QtCore.Qt.AlignCenter)
        self.label_id.setFont(labelFont)

        main_grid.addWidget(self.label_img, 0 , 0)
        main_grid.addWidget(self.label_name, 1 , 0)
        main_grid.addWidget(self.label_id, 2 , 0)

#################################################################


        if self.acceso[0] != '99':
            self.button_usuarios.setEnabled(False)
            if '1' not in self.acceso:
                self.button_aduana.setEnabled(False)
            if '2' not in self.acceso:
                self.button_rivian.setEnabled(False)


#################################################################


        self.button_aduana.triggered.connect(self.aduana)
        self.button_rivian.triggered.connect(self.rivian)
        self.button_salir.triggered.connect(self.salir)
        self.button_passwd.triggered.connect(self.show_pass)

#################################################################


    def show_pass(self):
        self.pass_wd = PasswdUi.Pass(self.nombre_completo, self.noreloj, self.passwd, self.database)
        self.pass_wd.update_password.connect(self.pass_update)
        self.pass_wd.show()

    def aduana(self):
        if self.aduan_ui:
            self.aduan_ui.showMaximized()
        else:
            self.aduan_ui = AduanaUi.Aduana(self.noreloj, self.nombre_completo, self.area, self.database, self.path)
            self.aduan_ui.showMaximized()

    def rivian(self):
        if self.rivian_ui:
            self.rivian_ui.showMaximized()
        else:
            self.rivian_ui = RivianUi.Rivian(self.noreloj, self.database, self.today, self.path)
            self.rivian_ui.showMaximized()

    def pass_update(self, new_pass):
        self.passwd = new_pass

    def closeEvent(self, event: QtGui.QCloseEvent):  # noqa: N802
        """
        Can be used to prevent Alt+F4 or other automatic closes.
        :param event: The close event
        """
        if self.close_callback == False:
            event.ignore()

    def salir(self):
        self.close_callback = True
        if self.pass_wd:
            self.pass_wd.close()
        if self.rivian_ui:
            self.rivian_ui.close()
        if self.aduan_ui:
            self.aduan_ui.close()
        self.close()

def main():
    app = QApplication(sys.argv)

    window = User(17040267, "Luis", "Castro", "M1", "Ingenieria", "Administrador")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
