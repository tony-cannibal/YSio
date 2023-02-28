import sys
from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
try:
    from . import constants as cn
    from . import functions as fn
except ImportError:
    import constants as cn
    import functions as fn



class Pass(QWidget):

    update_password = QtCore.pyqtSignal(str)

    def __init__(self, name, noreloj, password, database):
        super().__init__()

        self.name = name
        self.noreloj = noreloj
        self.password = password
        self.database = database

        self.setWindowTitle("Contraseña")
        # self.setFixedSize(QtCore.QSize(400, 370))
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        self.form_box = QGroupBox("Contraseña")
        box_layout = QFormLayout()


        self.user = QLineEdit(f'{self.name}')
        self.user.setEnabled(False)
        self.user.setAlignment(QtCore.Qt.AlignCenter)
        self.user.setStyleSheet(cn.line_label)

        self.no = QLineEdit(f'{self.noreloj}')
        self.no.setEnabled(False)
        self.no.setAlignment(QtCore.Qt.AlignCenter)
        self.no.setStyleSheet(cn.line_label)

        self.pasword_old = QLineEdit()
        self.pasword_old.setAlignment(QtCore.Qt.AlignCenter)
        self.pasword_old.setEchoMode(QLineEdit.Password)
        self.pasword_new = QLineEdit()
        self.pasword_new.setAlignment(QtCore.Qt.AlignCenter)
        self.pasword_new.setEchoMode(QLineEdit.Password)
        self.pasword_conf = QLineEdit()
        self.pasword_conf.setAlignment(QtCore.Qt.AlignCenter)
        self.pasword_conf.setEchoMode(QLineEdit.Password)

        box_layout.addRow("Nombre", self.user)
        box_layout.addRow("Num. Reloj", self.no)
        box_layout.addRow("Contrseña Anterior", self.pasword_old)
        box_layout.addRow("Contrseña Nueva", self.pasword_new)
        box_layout.addRow("ConfirmarContrseña", self.pasword_conf)

        self.form_box.setLayout(box_layout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.form_box)
        layout.addWidget(self.buttonBox)


        self.error = QMessageBox()
        self.error.setWindowTitle('Error')
        self.error.setIcon(QMessageBox.Critical)

        self.setLayout(layout)

    def accept(self):
        old_pass = self.pasword_old.text().strip()
        new_pass = self.pasword_new.text().strip()
        conf_pass = self.pasword_conf.text().strip()
        if self.pasword_old.text() == "":
            self.error.setText('Debes Introducir tu Contraseña.')
            self.error.exec_()
            return
        if old_pass != str(self.password):
            self.error.setText('Contraseña Incorrecta.')
            self.error.exec_()
            return
        if new_pass == old_pass:
            self.error.setText('No Puedes Usar La Misma Contraseña.')
            self.error.exec_()
            return
        if new_pass != conf_pass:
            self.error.setText('Tus Constraseñas No Coinciden.')
            self.error.exec_()
            return
        fn.update_password(self.noreloj, new_pass, self.database)
        self.password = new_pass
        self.update_password.emit(self.password)
        self.error.setIcon(QMessageBox.Warning)
        self.error.setWindowTitle('Advertencia')
        self.error.setText('La Contrseña A Sido Cambiada.')
        self.error.exec_()
        self.close()
        
        
    def reject(self):
        self.close()


def main(name, noreloj, passwd, db):
    app = QApplication(sys.argv)

    window = Pass(name, noreloj, passwd, db)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    db = {
        "host": "172.18.4.58",
        "database": "yura_elaboracion",
        "user": "yura_admin",
        "password": "Metallica24+",
        "port": 3306
        }

    name = 'Luis Antonio Castro Vital'
    noreloj = 17040267  
    passwd = 17040267  
    
    main(name, noreloj, passwd, db)