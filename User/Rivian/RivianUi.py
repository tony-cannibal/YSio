import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from datetime import datetime
import math
import os

try:
    from . import functions as fn
    from . import constants as cn
except ImportError:
    import functions as fn
    import constants as cn


class Rivian(QWidget):
    def __init__(self, noreloj, db, today, path):
        super().__init__()

        self.noreloj = noreloj
        self.database = db
        self.today = today
        self.path = path
        self.port = [fn.set_port() if fn.set_port() else '0']

        self.inventory = fn.get_riv_lots(self.database)
        self.history = fn.get_riv_inv(self.database, self.today)
        self.current = []
        self.rivian = []
        self.search = []
        self.result = []

        self.setWindowTitle("Aduana")
        self.setMinimumSize(800, 400)
        self.setStyleSheet(cn.qwidget_style)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setStyleSheet('''
        ''')

#########################################################################

        # Tab 1
        self.tab1 = QFrame()
        tab1_layout = QGridLayout()
        tab1_layout.setSpacing(0)
        self.tab1.setLayout(tab1_layout)

        self.frame1 = QFrame()
        self.frame1.setStyleSheet(cn.frame_style)
        self.frame1.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        frame1_layout = QGridLayout()
        self.frame1.setLayout(frame1_layout)

        tableFont = QFont(QFont('Consolas', 10))

        labelFont = QFont(QFont('Consolas', 12))
        labelFont.setBold(True)

        self.line_scan = QLineEdit()
        self.line_scan.setFont(labelFont)

        self.part_num = QLabel()
        self.part_num.setText('NP: ')
        self.part_num.setFont(labelFont)

        self.rev = QLabel()
        self.rev.setSizePolicy(QSizePolicy.Expanding,
                               QSizePolicy.Fixed)
        self.rev.setText('REV: ')
        self.rev.setFont(labelFont)

        self.lot = QLabel()
        self.lot.setText('LOT: ')
        self.lot.setFont(labelFont)

        self.item = QLabel()
        self.item.setText('ITEM: ')
        self.item.setFont(labelFont)

        self.piezas = QLabel()
        self.piezas.setText('PZ: ')
        self.piezas.setFont(labelFont)

        self.l_edit = QLineEdit()
        self.l_edit.setFont(labelFont)
        self.l_edit.setAlignment(QtCore.Qt.AlignCenter)

        self.pesar = QPushButton("&Pesar", self)
        self.pesar.setFont(labelFont)

        self.state = QLabel('Bascula Conectada')
        self.state.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.state.setStyleSheet('''
                                 border: 0px solid #000;
                                 color: green;
                                 ''')

        self.cant = QLabel()
        self.cant.setFont(labelFont)
        self.cant.setAlignment(QtCore.Qt.AlignCenter)
        self.cant.setText("0")

        self.artesa_chica = QRadioButton("Artesa Chica")
        self.artesa_chica.setChecked(True)
        self.artesa_grande = QRadioButton("Artesa Grande")
        self.sin_tara = QRadioButton("Sin Tara")

        self.table_1 = QTableWidget()
        self.table_1.setColumnCount(11)
        self.table_1.setAlternatingRowColors(True)
        self.table_1.setHorizontalHeaderLabels(cn.headers)
        for i in range(11):
            self.table_1.setColumnWidth(i, cn.header_width[i])
        self.table_1.verticalHeader().setVisible(False)
        self.table_1.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_1.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_1.setFont(tableFont)

        self.logo = QPixmap(f'{self.path}/src/rivian.png')
        self.label_logo = QLabel()
        self.label_logo.setStyleSheet('''
            border-style: solid;
            border-color: black;
            border-width: 0px;
            padding-right: 80px;
            border-image: none;
            background: none;
            ''')
        self.label_logo.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
        self.label_logo.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        # self.label_logo.setMaximumHeight(50)
        self.label_logo.setPixmap(self.logo.scaled(78, 78,
                                                   QtCore.Qt.KeepAspectRatio))

        self.spacer1 = QSpacerItem(
            30, 30, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacer2 = QSpacerItem(
            30, 30, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.row_spacer = QSpacerItem(
            30, 60, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.row_spacer2 = QSpacerItem(
            50, 50, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.row_spacer3 = QSpacerItem(
            30, 40, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.column_spacer = QSpacerItem(
            30, 30, QSizePolicy.Fixed, QSizePolicy.Fixed)




        # Widgets
        frame1_layout.addWidget(self.line_scan, 1, 1, 1, 3)
        frame1_layout.addWidget(self.label_logo, 0, 7, 2, 2)

        frame1_layout.addWidget(self.lot,      3, 1, 1, 2)
        frame1_layout.addWidget(self.part_num, 3, 4, 1, 2)
        frame1_layout.addWidget(self.rev,      3, 7, 1, 2)

        frame1_layout.addWidget(self.item,   5, 1, 1, 5)
        frame1_layout.addWidget(self.piezas, 5, 7, 1, 2)

        frame1_layout.addWidget(self.state,    6, 1, 1, 2)

        frame1_layout.addWidget(self.l_edit,   7, 4, 1, 2)
        frame1_layout.addWidget(self.pesar,    7, 1, 1, 2)
        frame1_layout.addWidget(self.cant,     7, 7, 1, 2)

        frame1_layout.addWidget(self.artesa_chica,  8, 1, QtCore.Qt.AlignTop)
        frame1_layout.addWidget(self.artesa_grande, 8, 2, QtCore.Qt.AlignTop)
        frame1_layout.addWidget(self.sin_tara,      8, 3, QtCore.Qt.AlignTop)

        frame1_layout.addWidget(self.table_1,  9, 1, 1, 8)

        # Spacers
        frame1_layout.addItem(self.row_spacer2, 0, 1)

        frame1_layout.addItem(self.spacer2, 1, 3, 1, 3)

        frame1_layout.addItem(self.row_spacer, 2, 1)
        frame1_layout.addItem(self.row_spacer, 2, 2)
        frame1_layout.addItem(self.row_spacer, 2, 3)
        frame1_layout.addItem(self.row_spacer, 2, 4)
        frame1_layout.addItem(self.row_spacer, 2, 5)
        frame1_layout.addItem(self.row_spacer, 2, 6)
        frame1_layout.addItem(self.row_spacer, 2, 7)
        frame1_layout.addItem(self.row_spacer, 2, 8)

        frame1_layout.addItem(self.row_spacer, 4, 1)
        frame1_layout.addItem(self.row_spacer, 6, 1)
        frame1_layout.addItem(self.row_spacer, 8, 1)

        frame1_layout.addItem(self.column_spacer, 1, 0)
        frame1_layout.addItem(self.column_spacer, 1, 9)

        frame1_layout.addItem(self.row_spacer, 10, 1)

########################################################

        # Frame 2 Tab 1
        self.frame2 = QFrame()
        self.frame2.setStyleSheet(cn.frame_style)
        self.frame2.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        frame2_layout = QGridLayout()

        self.search_line = QLineEdit()

        self.date1 = QDateTimeEdit(calendarPopup=True)
        self.date1.setDate(QDate(self.today[0], self.today[1], self.today[2]))
        self.date1.setDisplayFormat('yyyy-MM-dd')

        self.date2 = QDateTimeEdit(calendarPopup=True)
        self.date2.setDate(QDate(self.today[0], self.today[1], self.today[2]))
        self.date2.setDisplayFormat('yyyy-MM-dd')

        self.excel = QPushButton('Excel')

        self.table_history = QTableWidget()
        self.table_history.setColumnCount(12)
        self.table_history.setHorizontalHeaderLabels(cn.headers2)
        self.table_history.setAlternatingRowColors(True)
        for i in range(12):
            self.table_history.setColumnWidth(i, cn.header_width2[i])
        self.table_history.verticalHeader().setVisible(False)
        self.table_history.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_history.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)

        frame2_layout.addWidget(self.search_line, 1, 1, 1, 2)
        # frame2_layout.addWidget(self.date1, 1, 3)
        # frame2_layout.addWidget(self.date2, 1, 4)
        frame2_layout.addWidget(self.excel, 1, 6)

        frame2_layout.addWidget(self.table_history, 3, 1, 1, 6)

        frame2_layout.addItem(self.column_spacer, 0, 0)
        frame2_layout.addItem(self.row_spacer, 0, 1)
        frame2_layout.addItem(self.row_spacer, 0, 2)
        frame2_layout.addItem(self.row_spacer, 0, 3)
        frame2_layout.addItem(self.row_spacer, 0, 4)
        frame2_layout.addItem(self.row_spacer, 0, 5)
        frame2_layout.addItem(self.row_spacer, 0, 6)
        frame2_layout.addItem(self.column_spacer, 0, 7)

        frame2_layout.addItem(self.row_spacer, 2, 1)
        frame2_layout.addItem(self.row_spacer, 4, 1)

        self.frame2.setLayout(frame2_layout)

#########################################################################

        tab1_layout.addWidget(self.frame1, 0, 0)
        tab1_layout.addWidget(self.frame2, 0, 1)

#########################################################################

        # Tab 2
        self.tab2 = QFrame()
        self.tab2.setStyleSheet(cn.frame_style)
        tab2_layout = QGridLayout()
        self.tab2.setLayout(tab2_layout)

        self.file_button = QPushButton()
        self.file_button.setText("Buscar")

        self.file_label = QLabel()
        self.file_label.setText("Archivo:")
        self.file_label.setStyleSheet('''
            border: 1px solid black;
            background-color: #fff;
        ''')

        self.upload_button = QPushButton()
        self.upload_button.setText("Guardar")

        self.table3 = QTableWidget()
        self.table3.setColumnCount(11)
        self.table3.setHorizontalHeaderLabels(cn.headers3)
        for i in range(0, 11):
            self.table3.setColumnWidth(i, 150)
        self.table3.setAlternatingRowColors(True)
        self.table3.verticalHeader().setVisible(False)
        self.table3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table3.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        tab2_layout.addWidget(self.file_button, 1, 1)
        tab2_layout.addWidget(self.file_label, 1, 2)

        tab2_layout.addWidget(self.table3, 3, 1, 1, 7)

        tab2_layout.addWidget(self.upload_button, 1, 7)

        tab2_layout.addItem(self.column_spacer, 0, 0)
        tab2_layout.addItem(self.row_spacer3, 0, 1)
        tab2_layout.addItem(self.row_spacer3, 0, 2)
        tab2_layout.addItem(self.row_spacer3, 0, 3)
        tab2_layout.addItem(self.row_spacer3, 0, 4)
        tab2_layout.addItem(self.row_spacer3, 0, 5)
        tab2_layout.addItem(self.row_spacer3, 0, 6)
        tab2_layout.addItem(self.row_spacer3, 0, 7)
        tab2_layout.addItem(self.column_spacer, 0, 8)

        tab2_layout.addItem(self.row_spacer3, 2, 1)

        tab2_layout.addItem(self.row_spacer3, 4, 1)

        tab2_layout.addItem(self.row_spacer3, 6, 1)


#########################################################################

        self.tab_widget.addTab(self.tab1, 'Rivian')
        self.tab_widget.addTab(self.tab2, 'Administracion')

        layout.addWidget(self.tab_widget)
        self.update_history()

        self.error = QMessageBox()
        self.error.setWindowTitle('Error')
        self.error.setIcon(QMessageBox.Critical)

        self.info = QMessageBox()
        self.info.setWindowTitle('Error')
        self.info.setIcon(QMessageBox.Information)

        self.line_scan.setFocus()


#########################################################################

        # Connections

        self.line_scan.returnPressed.connect(self.read_code)

        self.pesar.clicked.connect(self.ob_peso)

        self.file_button.clicked.connect(self.get_file_input)

        self.upload_button.clicked.connect(self.save_input)
        self.l_edit.textChanged.connect(self.convert_weight)
        self.artesa_chica.toggled.connect(self.convert_weight)
        self.artesa_grande.toggled.connect(self.convert_weight)
        self.sin_tara.toggled.connect(self.convert_weight)
        self.l_edit.returnPressed.connect(self.save_record)
        self.search_line.returnPressed.connect(self.find_records)
        self.excel.clicked.connect(self.export_excel)

        if self.port[0] == '0':
            self.error.setText('No se a detectado ninguna bascula.')
            self.error.exec_()
            self.state.setText('Bascula Desconectada.')
            self.state.setStyleSheet('color: red; border-width: 0px;')

#########################################################################

    # Functions
    def port_message_bad(self):
        self.error.setText('La Bascula se a Desconectado.')
        self.error.exec_()
        self.state.setText('Bascula Desconectada.')
        self.state.setStyleSheet('color: red; border-width: 0px;')

    def port_message_good(self):
        self.error.setText('La Bascula se a Conectado.')
        self.error.exec_()
        self.state.setText('Bascula Conectada.')
        self.state.setStyleSheet('color: green; border-width: 0px;')

    def update_table3(self):
        self.table3.setRowCount(len(self.rivian))
        # row_labels = []
        tablerow = 0
        for row in self.rivian:
            for i in range(11):
                self.table3.setItem(
                    tablerow, i, QtWidgets.QTableWidgetItem(str(row[i])))
                self.table3.item(tablerow, i).setTextAlignment(
                    QtCore.Qt.AlignCenter)
            tablerow += 1

    def update_history(self):
        self.table_1.setRowCount(len(self.history))
        tablerow = 0
        for row in self.history:
            for i in range(11):
                self.table_1.setItem(
                    tablerow, i, QtWidgets.QTableWidgetItem(str(row[i+1])))
                self.table_1.item(tablerow, i).setTextAlignment(
                    QtCore.Qt.AlignCenter)
            tablerow += 1

    def update_table_search(self):
        self.table_history.setRowCount(len(self.result))
        tablerow = 0
        for row in self.result:
            for i in range(12):
                self.table_history.setItem(
                    tablerow, i, QtWidgets.QTableWidgetItem(str(row[i])))
                self.table_history.item(tablerow, i).setTextAlignment(
                    QtCore.Qt.AlignCenter)
            tablerow += 1

    def find_records(self):
        query = self.search_line.text()
        self.result = fn.inv_search(query, self.database)
        self.update_table_search()

    def update_labels(self):
        self.part_num.setText('NP:' + f'{self.current[6]}'.center(15, ' '))
        self.lot.setText('LOT:' + f'{self.current[0]}'.center(15, ' '))
        self.rev.setText('REV:' + f'{self.current[7]}'.center(12, ' '))
        self.item.setText('ITEM:' + f'{self.current[4]}'.center(44, ' '))
        self.piezas.setText('PZ:' + f'{self.current[8]}'.center(14, ' '))

    def clean_labels(self):
        self.part_num.setText('NP: ')
        self.lot.setText('LOT: ')
        self.rev.setText('REV: ')
        self.piezas.setText('PZ: ')
        self.item.setText(f'ITEM: ')

    def read_code(self):
        code = self.line_scan.text().strip()
        self.inv_error = QMessageBox()
        self.inv_error.setWindowTitle('Error')
        self.inv_error.setIcon(QMessageBox.Critical)
        if code == '':
            return
        if len(code) > 10:
            lot = code[1:-1].split(';')[0]
        else:
            lot = code
        if lot not in self.inventory:
            result = fn.lot_search(lot, self.database)
            if result != None:
                search = list(result)
                search[2] = search[2].strftime("%Y-%m-%d")
                self.current = search
                self.update_labels()
            else:
                self.current = []
                self.clean_labels()
                self.inv_error.setText(
                    'El lote no se encuentra enla base de Datos')
                self.inv_error.exec_()
                self.line_scan.setFocus()
        else:
            self.inv_error.setText(f'El Lote {lot} ya tiene entrada.')
            self.inv_error.exec_()
        self.line_scan.setText("")

    def get_file_input(self):
        try:
            file = QFileDialog.getOpenFileName(
                self, caption='Buscar Archivo',
                directory='/'.join(os.path.expanduser('~').split('\\')
                                   )+'/Documents',
                filter="Excel (*.xlsx)", options=QFileDialog.Options())
            file = file[0]

            part = fn.get_riv_part(self.database)
            self.rivian = fn.get_riv_input_2(file, part)
            file = file[1:].split('/')[-1]
            self.file_label.setText(
                f'Archivo: <font color="blue">  {file}</font>')
            self.update_table3()
        except FileNotFoundError:
            pass

    def save_input(self):
        input_data = fn.get_database_input(self.database)
        if self.rivian:
            duplicates = [i[0] for i in self.rivian if i[0] in input_data]
            for i in self.rivian:
                if i[0] not in duplicates:
                    fn.save_input(i, self.database)
                    self.rivian = []
                    self.update_table3()
                    self.file_label.setText('Archivo: ')

            if len(duplicates) == 0:
                self.info.setText('El Input se a Guardado.')
                self.info.exec_()
            elif len(duplicates) == len(self.rivian):
                self.error.setText('Todos los lotes son duplicados.')
                self.error.exec_()
            else:
                self.info.setText('Algunos lotes son duplicados.')
                self.info.exec_()
        else:
            self.error.setText('No hay nada para guardar.')
            self.error.exec_()

    def convert_weight(self):
        weight = self.l_edit.text().strip()
        if not weight:
            return
        if self.current:
            if len(weight) == 1 and not weight.isnumeric():
                self.l_edit.setText('')
            elif weight.count('.') > 1:
                self.l_edit.setText(weight[:-1])
            elif weight[-1].isalpha():
                self.l_edit.setText(weight[:-1])
            elif weight[-1] in cn.simbols:
                self.l_edit.setText(weight[:-1])
            else:
                if self.artesa_chica.isChecked():
                    tara = 1.713
                elif self.artesa_grande.isChecked():
                    tara = 3.16
                else:
                    tara = 0
                peso = float(weight)
                resultado = math.ceil((peso - tara) / self.current[-1])
                self.cant.setText(str(resultado))
                now = datetime.now().strftime('%H:%M:%S')
        else:
            # self.l_edit.setText('')
            pass

    def save_record(self):
        cantidad = self.cant.text()
        if not self.current:
            return
        if int(cantidad) <= 0:
            self.error.setText(
                'El valor debe coincidir con el valor de piezas')
            self.error.exec_()
            return
        now = datetime.now().strftime('%H:%M:%S')
        peso = self.l_edit.text()
        date = datetime(
            year=self.today[0], month=self.today[1], day=self.today[2]).strftime('%Y-%m-%d')
        # if int(cantidad) == self.current[8]:
        record = [
            self.noreloj, self.current[0], self.current[2], self.current[6], self.current[7],
            self.current[3], self.current[4], self.current[5], now, date, peso, cantidad
        ]
        fn.upload_record(record, self.database)
        self.history.append(record)
        self.clean_labels()
        self.l_edit.setText('0')
        self.update_history()
        self.inventory.append(self.current[0])
        self.current = []
        self.cant.setText('0')
        # else:
        #     self.error.setText(
        #         'El valor debe coincidir con el valor de piezas')
        #     self.error.exec_()

    def ob_peso(self):
        if self.port[0] == '0':
            self.port = [fn.set_port() if fn.set_port() else '0']
            if self.port[0] != '0':
                self.port_message_good()
        if self.port[0] == '0':
            weight = '0'
        else:
            try:
                weight = fn.read_weight(self.port[0])
            except:
                self.port = '0'
                self.port_message_bad()
                weight = '0'
        self.l_edit.setText(weight)
        self.l_edit.setFocus()

    def export_excel(self):
        if self.result:
            save_name = QFileDialog.getSaveFileName(
                self, caption='Guardar Archivo',
                directory='/'.join(os.path.expanduser('~').split('\\')
                                   )+'/Documents',
                filter="Excel (*.xlsx)"
            )
            fn.export_data(self.result, save_name[0])
        else:
            save_error = QMessageBox()
            save_error.setWindowTitle('Error')
            save_error.setText('No Hay Contenido Para Guardar')
            save_error.setIcon(QMessageBox.Warning)
            save_error.exec_()


def main():
    db = {
        "host": "172.18.4.58",
        "database": "yura_elaboracion",
        "user": "yura_admin",
        "password": "Metallica24+",
        "port": 3306
    }
    path = 'C:/Users/YR PROD ORDER/Documents/Python/YSio - MariaDB'
    app = QApplication(sys.argv)
    window = Rivian(17040267, db, [2023, 1, 25], path)
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
