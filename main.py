import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from Login import LoginUi
from Inventory import InventoryUi
from User import UserUi
import setup as db


class Controller:
    def __init__(self):
        self.path = "/".join(os.getcwd().split("\\"))
        self.database = db.database(True)
        self.window = None
        self.login = None
        self.aduana = None
        self.user = None

    def show_login(self):
        self.login = LoginUi.Login(self.path, self.database)
        self.login.setStyleSheet(
            """
            background: black;
                 """
        )
        self.login.switch_window.connect(self.show_main)
        self.login.switch_window_user.connect(self.show_user)
        self.login.show()

    def show_main(self, equipo, port):
        self.window = InventoryUi.Inventory(
            equipo, port, self.path, self.database
        )
        self.login.close()
        self.window.show()
        self.window.showFullScreen()

    def show_user(self, user):
        self.user = UserUi.User(user, self.path, self.database)
        self.login.close()
        self.user.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
