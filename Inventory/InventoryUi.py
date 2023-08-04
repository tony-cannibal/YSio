import sys
# from datetime import date
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QFrame, QGridLayout, QSizePolicy, QLabel, QLineEdit, QTableWidget,
    QRadioButton, QPushButton, QCheckBox, QComboBox, QSpacerItem,
    QMessageBox, QApplication,
)
try:
    from . import functions as fn
    from . import constants as cn
except ImportError:
    import functions as fn
    import constants as cn


class Inventory(QFrame):
    def __init__(self, equipo, port, path, database):
        super().__init__()

        self.name = equipo[0]
        self.area = equipo[1]
        self.sub_area = equipo[2]
        self.equipo = equipo[3]
        self.config = {
            "manualInput": bool(equipo[4]),
            "radioReset": bool(equipo[5])
        }
        # self.manual = bool(equipo[4])
        self.port = port
        self.root_path = path
        self.database = database
        self.materials = {}
        cable = self.sub_area[:5]

        self.warning = None
        self.high_weight = None

        self.setStyleSheet(cn.theme)

        if cable.lower() != "cable":
            for i in fn.get_materiales(self.database):
                self.materials[i[2]] = i
        else:
            for i in fn.get_materiales_cables(self.database):
                self.materials[i[2]] = i

        self.current_sel = []
        self.history = []
        self.code = []
        self.master = fn.check_master(self.equipo)
        self.service = fn.check_service(self.equipo)
        # self.manual = fn.manual_input(self.database, self.master)

        # self.setStyleSheet('background-color: black;')

        main_grid = QGridLayout()
        main_grid.setSpacing(0)
        self.setLayout(main_grid)

        self.frame_1 = QFrame()
        self.frame_1.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frame_2 = QFrame()
        self.frame_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_grid.addWidget(self.frame_1, 0, 0)
        main_grid.addWidget(self.frame_2, 0, 1)

        grid_1 = QGridLayout()

        grid_2 = QGridLayout()
        grid_2.setColumnMinimumWidth(0, 40)
        grid_2.setColumnMinimumWidth(1, 130)
        grid_2.setColumnMinimumWidth(3, 130)
        grid_2.setColumnMinimumWidth(4, 40)
        grid_2.setRowMinimumHeight(0, 30)
        grid_2.setRowMinimumHeight(2, 20)
        grid_2.setRowMinimumHeight(7, 20)

        ######################################################################

        # Frame 1
        self.frame_1.setLayout(grid_1)
        self.frame_1.setStyleSheet(fn.set_style(self.name))

        # Frame 1 Items
        self.line_1 = QLineEdit()
        self.line_1.setFont(QFont("Consolas", 14))
        self.line_1.setStyleSheet(cn.line_theme)
        if self.config["manualInput"] is False:
            self.line_1.setEchoMode(QLineEdit.Password)

        self.line_2 = QLineEdit()
        self.line_2.setFont(QFont("Consolas", 14))
        self.line_2.setMaximumWidth(150)
        self.line_2.setAlignment(QtCore.Qt.AlignCenter)
        self.line_2.setStyleSheet(
            """
            padding-top: 6px;
            padding-bottom: 6px;
            """
        )
        self.table_1 = QTableWidget()
        self.table_1.setStyleSheet(cn.theme)
        self.table_1.setColumnCount(3)
        self.table_1.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_1.setHorizontalHeaderLabels(["Yura", "Tipo", "Provedor"])
        self.table_1.setColumnWidth(0, 100)
        self.table_1.setColumnWidth(1, 60)
        self.table_1.setColumnWidth(2, 120)
        self.table_1.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.table_1.verticalHeader().setMinimumWidth(30)
        # self.table_1.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.table_1.setFont(QFont("Consolas", 8))
        self.table_1.verticalHeader().setVisible(False)

        self.label_main = QLabel()
        self.label_main.setText(f"Inventario Mensual: {self.name}")
        mainfont = QFont("Consolas", 16)
        mainfont.setBold(True)
        self.label_main.setFont(mainfont)
        self.label_main.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main.setStyleSheet(
            """
            background-color: white;
            border: 1px solid #000;
            border-radius: 2px;
            """
        )
        labelfont = QFont(QFont("Consolas", 17))
        labelfont.setBold(True)

        self.label_1_1 = QLabel()
        # self.label_1_1.setText("Provedor")
        self.label_1_1.setText("")
        self.label_1_1.setFont(QFont(labelfont))
        self.label_1_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_1.setStyleSheet(cn.mat_label_theme)

        self.label_1_2 = QLabel()
        # self.label_1_2.setText("Yura")
        self.label_1_2.setText("")
        self.label_1_2.setFont(QFont(labelfont))
        self.label_1_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_2.setStyleSheet(cn.mat_label_theme)

        self.label_1_3 = QLabel()
        # self.label_1_3.setText("Tipo")
        self.label_1_3.setText("")
        self.label_1_3.setFont(QFont(labelfont))
        self.label_1_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_3.setStyleSheet(cn.mat_label_theme)

        self.label_1_4 = QLabel()
        # self.label_1_4.setText("Pkg")
        self.label_1_4.setText("")
        self.label_1_4.setFont(QFont(labelfont))
        self.label_1_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_4.setStyleSheet(cn.mat_label_theme)

        self.label_amount = QLabel()
        self.label_amount.setText("")
        self.label_amount.setMaximumWidth(150)
        self.label_amount.setFont(QFont("Consolas", 14))
        self.label_amount.setAlignment(QtCore.Qt.AlignCenter)
        self.label_amount.setStyleSheet(
            """
            background-color: #fff;
            border-bottom: 2px solid #000;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            """
        )
        radiofont = QFont("Consolas", 10)
        radiofont.setBold(True)

        self.radio1 = QRadioButton()
        self.radio1.setFont(QFont(radiofont))
        self.radio1.setText("Peso")
        self.radio1.setStyleSheet(cn.theme)
        self.radio2 = QRadioButton()
        self.radio2.setFont(QFont(radiofont))
        self.radio2.setText("Nuevo")
        self.radio2.setStyleSheet(cn.theme)
        self.radio3 = QRadioButton()
        self.radio3.setFont(QFont(radiofont))
        self.radio3.setText("Cantidad")
        self.radio3.setStyleSheet(cn.theme)

        self.button_1 = QPushButton("Pesar")
        self.button_1.setFont(QFont("Consolas", 14))
        self.button_1.setStyleSheet(cn.theme)

        self.box_1 = QCheckBox()
        self.box_1.setFont(QFont(radiofont))
        self.box_1.setText("Tara")
        self.box_1.setStyleSheet(cn.theme)

        self.combo = QComboBox()
        self.combo.setStyleSheet(cn.theme)
        self.combo.setFont(QFont("Consolas", 16))
        self.combo.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.logo = QPixmap(f"{self.root_path}/src/logo-rojo-v2.png")
        self.label_img = QLabel()
        self.label_img.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_img.setStyleSheet("border-width: 0px;")
        self.label_img.setPixmap(self.logo.scaled(
            66, 66, QtCore.Qt.KeepAspectRatio))
        self.label_img.setMaximumSize(100, 40)

        font2 = QFont(QFont("Consolas", 12))
        font2.setBold(True)

        self.codigo_yura = QLabel("Codigo Yura")
        self.codigo_yura.setFont(font2)
        self.codigo_yura.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.codigo_yura.setStyleSheet("padding-bottom: 0px;")

        self.codigo_proveedor = QLabel("Codigo Proveedor")
        self.codigo_proveedor.setFont(font2)
        self.codigo_proveedor.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.codigo_proveedor.setStyleSheet("padding-bottom: 0px;")

        self.tipo = QLabel("Tipo")
        self.tipo.setFont(font2)
        self.tipo.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.tipo.setStyleSheet("padding-bottom: 0px;")

        self.packing = QLabel("Packing")
        self.packing.setFont(font2)
        self.packing.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.packing.setStyleSheet("padding-bottom: 0px;")

        self.status = QLabel("Bascula Conectada")
        self.status.setFont(font2)
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        self.spacer = QSpacerItem(
            30, 30, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacer1 = QSpacerItem(
            30, 30, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.spacer2 = QSpacerItem(
            30, 30, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.spacer3 = QSpacerItem(
            25, 25, QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add Items to Frame 1
        grid_1.addWidget(self.label_main, 1, 1, 1, 6)
        grid_1.addWidget(self.label_img, 1, 7, QtCore.Qt.AlignRight)

        grid_1.addWidget(self.line_1, 3, 1, 1, 3)
        grid_1.addWidget(self.combo, 3, 6, 1, 2, QtCore.Qt.AlignRight)

        grid_1.addWidget(self.codigo_yura, 4, 5)

        grid_1.addWidget(self.table_1, 5, 1, 18, 3)

        grid_1.addWidget(self.label_1_1, 5, 5, 1, 3)
        grid_1.addWidget(self.codigo_proveedor, 6, 5)
        grid_1.addWidget(self.label_1_2, 7, 5, 1, 3)
        grid_1.addWidget(self.tipo, 8, 5)
        grid_1.addWidget(self.label_1_3, 9, 5, 1, 3)
        grid_1.addWidget(self.packing, 10, 5)
        grid_1.addWidget(self.label_1_4, 11, 5, 1, 3)

        grid_1.addWidget(self.radio1, 15, 5, QtCore.Qt.AlignCenter)
        grid_1.addWidget(self.radio2, 15, 6, QtCore.Qt.AlignCenter)
        grid_1.addWidget(self.radio3, 15, 7, QtCore.Qt.AlignCenter)

        grid_1.addWidget(self.box_1, 16, 5, QtCore.Qt.AlignCenter)
        grid_1.addWidget(self.line_2, 19, 5)
        grid_1.addWidget(self.button_1, 19, 6, 1, 2)
        grid_1.addWidget(self.status, 20, 6, 1, 2)
        grid_1.addWidget(self.label_amount, 20, 5)

        grid_1.addItem(self.spacer3, 0, 0)

        grid_1.addItem(self.spacer2, 0, 1)
        grid_1.addItem(self.spacer2, 0, 2)
        grid_1.addItem(self.spacer2, 0, 3)
        grid_1.addItem(self.spacer3, 0, 4)
        grid_1.addItem(self.spacer2, 0, 5)
        grid_1.addItem(self.spacer2, 0, 6)
        grid_1.addItem(self.spacer2, 0, 7)

        grid_1.addItem(self.spacer3, 0, 8)

        grid_1.addItem(self.spacer3, 2, 0)
        grid_1.addItem(self.spacer3, 4, 0)
        grid_1.addItem(self.spacer3, 6, 0)
        grid_1.addItem(self.spacer3, 12, 0)
        grid_1.addItem(self.spacer3, 13, 0)
        grid_1.addItem(self.spacer3, 14, 0)
        grid_1.addItem(self.spacer3, 17, 0)

        grid_1.addItem(self.spacer1, 22, 5)

        grid_1.addItem(self.spacer3, 23, 1)

        self.scale_message = QMessageBox()

        self.error = QMessageBox()
        self.error.setWindowTitle("Error")
        self.error.setText("Cantidad No Valida")
        self.error.setInformativeText(
            "La cantidad no debe ser menor o igual a '0'.")
        self.error.setIcon(QMessageBox.Critical)

        self.con_error = QMessageBox()
        self.con_error.setWindowTitle("Error")
        self.con_error.setText("La Bascula se a Desconectado")
        self.con_error.setInformativeText(
            "Verifica que la bascula este connectada correctamente."
        )
        self.con_error.setIcon(QMessageBox.Critical)

        #######################################################################

        # Frame 2 Items
        self.frame_2.setLayout(grid_2)
        self.frame_2.setStyleSheet(
            """
            background: White;
            border-style: solid;
            border-color: black;
            border-width: 1px;
            """
        )

        self.label_2_1 = QLabel()
        self.label_2_1.setText("Historial de Inventario")
        self.label_2_1.setFont(QFont("Consolas", 14))
        self.label_2_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2_1.setStyleSheet(
            """
            background-color: white;
            border: 0px solid white;
            """
        )

        self.table_2 = QTableWidget()
        self.table_2.setStyleSheet(cn.theme)
        self.table_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_2.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_2.setColumnCount(8)
        self.table_2.setHorizontalHeaderLabels(cn.table2_headers)
        self.table_2.setColumnWidth(0, 80)
        self.table_2.setColumnWidth(1, 120)
        self.table_2.setColumnWidth(2, 80)
        self.table_2.setColumnWidth(3, 80)
        self.table_2.setColumnWidth(4, 80)
        self.table_2.setColumnWidth(5, 90)
        self.table_2.setColumnWidth(6, 100)
        self.table_2.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_2.setFont(QFont("Consolas", 11))

        # Add Items to Frame 2
        grid_2.addWidget(self.label_2_1, 1, 2)
        grid_2.addWidget(self.table_2, 3, 1, 4, 3)

        #######################################################################

        # Set Default States
        self.radio1.setChecked(True)
        self.box_1.setChecked(True)

        self.box_1.setEnabled(self.master)
        self.box_1.setEnabled(self.service)

        self.radio2.setEnabled(not fn.check_cable(cable))
        self.radio3.setEnabled(not fn.check_cable(cable))

        #######################################################################

        # print(self.equipo)
        # Function Connections
        self.line_1.returnPressed.connect(self.search)
        self.table_1.itemSelectionChanged.connect(self.table_update_label)
        self.line_2.textChanged.connect(self.get_amount)
        self.radio1.toggled.connect(self.get_amount)
        self.radio2.toggled.connect(self.get_amount)
        self.radio2.toggled.connect(self.pkg_warning)
        self.box_1.toggled.connect(self.get_amount)
        self.line_2.returnPressed.connect(self.save_record)
        self.button_1.clicked.connect(self.get_weight)
        self.combo.currentIndexChanged.connect(self.get_machine_hist)

        #######################################################################

        # Autorun Functions
        self.maquinas = fn.get_machines(
            self.area, self.sub_area, self.database)
        if not fn.check_cable(cable):
            self.combo.addItem("")
        for i in self.maquinas:
            self.combo.addItem(f" {i[0]}  ")

        if self.port == "0":
            self.status.setText("Bascula Desconectada")
            self.status.setStyleSheet("color: red;")

        # self.search()

    ###########################################################################

    # Declare Functions
    def scale_status_err(self):
        self.status.setStyleSheet("color: red;")
        self.status.setText("Bascula Desconectada")
        self.scale_message.setWindowTitle("Error")
        self.scale_message.setIcon(QMessageBox.Critical)
        self.scale_message.setText("La Bascula Se A Desconectado.")
        self.scale_message.exec_()

    def scale_status_ok(self):
        self.status.setStyleSheet("color: black;")
        self.status.setText("Bascula Conectada")
        self.scale_message.setWindowTitle("Advertencia")
        self.scale_message.setIcon(QMessageBox.Information)
        self.scale_message.setText("La Bascula Se A Conectado.")
        self.scale_message.exec_()

    def pkg_warning(self):
        if self.radio2.isChecked():
            self.warning = QMessageBox()
            self.warning.setWindowTitle("Advertencia")
            self.warning.setIcon(QMessageBox.Information)
            self.warning.setText(
                "Verifica El Valor del Pkg Antes de Continuar.")
            self.warning.setInformativeText(
                "Si el valor del pkg no coincide con la cantidad especificada"
                "en la etiqueta del articulo debera introducir la cantidad del"
                'mismo como "cantidad".'
            )
            self.warning.exec_()

    def search(self):
        code = self.line_1.text().strip()
        first_char = code[0] if code != '' else ''
        length = len(code)
        if (self.config["manualInput"] is False and
                first_char != 'P' and
                length < 20 and 'Q' not in code and "S" not in code):
            codig_no_permitido = QMessageBox()
            codig_no_permitido.setWindowTitle("Error de Codigo")
            codig_no_permitido.setText("Codigo Manual No Permitido.")
            codig_no_permitido.setInformativeText(
                "Esta prohibido introducir codigos manualmente."
            )
            codig_no_permitido.setIcon(QMessageBox.Critical)
            codig_no_permitido.exec_()
            self.line_1.setText('')
            return

        self.code = fn.get_code_elements(self.line_1.text().strip())
        res = fn.search_mats(self.materials, self.code[1])
        self.table_1.setRowCount(len(res))
        tablerow = 0
        for row in res:
            self.table_1.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(row[2]))
            self.table_1.item(tablerow, 0).setTextAlignment(
                QtCore.Qt.AlignCenter)
            self.table_1.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(row[4]))
            self.table_1.item(tablerow, 1).setTextAlignment(
                QtCore.Qt.AlignCenter)
            self.table_1.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.table_1.item(tablerow, 2).setTextAlignment(
                QtCore.Qt.AlignCenter)
            self.table_1.setRowHeight(tablerow, 20)
            tablerow += 1
        self.table_1.setCurrentCell(1, 0)
        self.table_1.setCurrentCell(0, 0)

        # if len(res) != 0:
        #     self.line_1.setText("")
        self.line_1.setText("")
        if len(res) == 0:
            self.current_sel = []
            self.table_update_label()

        self.line_2.setFocus()

    def table_update_label(self):
        sel = self.table_1.currentRow()
        if sel != -1:
            yura = self.table_1.item(sel, 0).text()
            # barra = self.table_1.item(sel, 2).text()
            self.current_sel = list(self.materials[yura])
        # else:
        # print("No Match Found")
        self.current_sel = fn.check_pkg(self.current_sel, self.code)
        # print(self.current_sel)

        if len(self.current_sel) == 9:
            #
            self.label_1_1.setText(f"{self.current_sel[2]}")
            self.label_1_2.setText(f"{self.current_sel[3]}")
            self.label_1_3.setText(f"{str(self.current_sel[4])}")
            self.label_1_4.setText(f"{str(self.current_sel[7])}")
        else:
            self.label_1_1.setText("")
            self.label_1_2.setText("")
            self.label_1_3.setText("")
            self.label_1_4.setText("")

        self.line_1.setText("")
        self.line_2.setText("")
        self.label_amount.setText("0")

        if self.radio2.isChecked():
            try:
                self.label_amount.setText(str(self.current_sel[7]))
            except IndexError:
                self.label_amount.setText("")

    def get_amount(self):
        '''Calculate the amount.'''
        if not self.current_sel:

            self.line_2.setText("0")
            # return
        weight = self.line_2.text().strip()
        # print(self.current_sel)

        if self.radio2.isChecked():
            if not self.current_sel:
                self.label_amount.setText('0')
                return
            else:
                self.label_amount.setText(str(self.current_sel[7]))
                return

        if not weight:
            return

        if len(weight) == 1 and not weight.isnumeric():
            self.line_2.setText("")
            return

        if weight.count(".") > 1:
            self.line_2.setText(weight[:-1])
            return

        if weight[-1].isalpha():
            self.line_2.setText(weight[:-1])
            return

        if weight[-1] in cn.simbols:
            self.line_2.setText(weight[:-1])
            return

        if self.radio1.isChecked():
            if len(self.current_sel) == 0:
                return 0
            peso = weight
            if peso == "":
                peso = 0
            else:
                peso = float(peso)
            tipo = self.current_sel[4]
            if not self.box_1.isChecked():
                tara = 0
            else:
                tara = self.current_sel[8]
            peso_ind = self.current_sel[5]
            resultado = round(
                fn.calc_amount(
                    tipo=tipo, weight=peso, ind_weight=peso_ind, tara=tara
                ),
                0,
            )
            self.label_amount.setText(str(resultado))
            return
        self.label_amount.setText(self.line_2.text())

    def save_record(self):
        maquina = self.combo.currentText().strip()
        peso = "0" if self.line_2.text() == '' else self.line_2.text()
        # print(len(self.current_sel))
        if len(self.current_sel) != 0:
            if maquina != "" or self.master:
                if float(self.label_amount.text()) > 0:
                    value = ""
                    if self.radio1.isChecked():
                        value = "Peso"
                    if self.radio2.isChecked():
                        value = "Nuevo"
                    if self.radio3.isChecked():
                        value = "Cantidad"
                # provedor, yura, tipo, cantidad, peso,  area, maquina, fecha
                    # print(self.current_sel)
                    limit = cn.weight_limit[self.current_sel[4]]
                    ob = [
                        self.current_sel[3],  # Codigo de Proveedor
                        self.current_sel[2],  # Codigo Yura
                        self.current_sel[4],  # Tipo
                        self.label_amount.text(),  # Cantidad
                        maquina,  # Maquina
                        peso,  # Peso
                        self.name,  # Area
                        # date.today().strftime("%Y-%m-%d"),  # Fecha
                        value,  # Valor
                        self.code[0],  # Codigo
                        self.equipo,
                    ]
                    # print(ob)
                    if float(peso) < limit or value != "Peso":
                        # self.history.append(ob)
                        fn.capture_value(
                            ob, self.equipo, self.sub_area.split()[
                                0], self.database
                        )
                        self.get_machine_hist()
                        self.line_1.setText("")
                        self.line_2.setText("")
                        self.label_amount.setText("0")
                        self.table_1.clearContents()
                        self.table_1.setRowCount(0)
                        if self.config["radioReset"] is True:
                            self.radio1.setChecked(True)
                        self.current_sel = []
                        self.table_update_label()
                        self.line_1.setFocus()
                    else:
                        high_weight = QMessageBox()
                        high_weight.setWindowTitle("Error de Peso")
                        high_weight.setText("Peso Demaciado Alto.")
                        high_weight.setInformativeText(
                            "Verifica el estado de la bascula y del material."
                        )
                        high_weight.setIcon(QMessageBox.Critical)
                        high_weight.exec_()
                        self.line_2.setText('')
                else:
                    self.error.exec_()
            else:
                error_maquina = QMessageBox()
                error_maquina.setWindowTitle("Error de Maquina.")
                error_maquina.setText(
                    "No as seleccionado una 'Maquina'.")
                error_maquina.setInformativeText(
                    """Debes seleccionar un numero de maquina para poder
                    guardar el registro."""
                )
                error_maquina.setIcon(QMessageBox.Critical)
                error_maquina.exec_()

    def display_history(self):

        self.table_2.setRowCount(len(self.history))
        # print(self.history)
        row_labels = []
        tablerow = 0
        for row in self.history:
            # Yura
            self.table_2.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.table_2.item(tablerow, 0).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # Proveedor
            self.table_2.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.table_2.item(tablerow, 1).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # Cantidad
            self.table_2.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.table_2.item(tablerow, 2).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # peso
            self.table_2.setItem(
                tablerow, 3, QtWidgets.QTableWidgetItem(str(row[4])))
            self.table_2.item(tablerow, 3).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # Maquina
            self.table_2.setItem(
                tablerow, 4, QtWidgets.QTableWidgetItem(str(row[5])))
            self.table_2.item(tablerow, 4).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # Equipo
            self.table_2.setItem(
                tablerow, 5, QtWidgets.QTableWidgetItem(str(row[6])))
            self.table_2.item(tablerow, 5).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # Valor
            self.table_2.setItem(
                tablerow, 6, QtWidgets.QTableWidgetItem(row[8]))
            self.table_2.item(tablerow, 6).setTextAlignment(
                QtCore.Qt.AlignCenter)
            self.table_2.setItem(
                tablerow, 7, QtWidgets.QTableWidgetItem(row[10]))
            self.table_2.item(tablerow, 7).setTextAlignment(
                QtCore.Qt.AlignCenter)
            # self.table_2.setRowHeight(tablerow, 20)
            tablerow += 1
        for i in range(len(self.history)):
            row_labels.append(str(i + 1) + "  ")
        self.table_2.setVerticalHeaderLabels(row_labels)
        self.table_2.setCurrentCell(len(self.history) - 1, 0)

    def get_weight(self):
        if self.port == "0":
            port = [fn.set_port() if fn.set_port() else "0"]
            if port[0] != "0":
                self.port = port[0]
                self.scale_status_ok()

        if self.port == "0":
            weight = "0"
        else:
            try:
                weight = fn.read_weight(self.port)
            except FileNotFoundError:
                self.port = "0"
                self.scale_status_err()
                weight = "0"
        self.line_2.setText("")
        self.line_2.setText(weight)
        self.line_2.setFocus()

    def get_machine_hist(self):
        maquina = self.combo.currentText().strip()
        history = fn.get_history(maquina, self.equipo, self.database)
        # if len(history) > 0:
        self.history = history
        self.display_history()
        # print(history)


def main():
    db = {
        "host": "172.18.4.58",
        "database": "yura_elaboracion",
        "user": "yura_admin",
        "password": "Metallica24+",
        "port": 3306,
    }
    path = "C:/Users/YR PROD ORDER/Documents/Python/YSio - MariaDB"
    app = QApplication(sys.argv)
    window = Inventory("Corte M1", "M1", "corte", "Master", "0", path, db)
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
