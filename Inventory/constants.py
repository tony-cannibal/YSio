

areas = ['Corte M1', 'Medios M1', 'Corte M2', 'Medios M2',
         'BATTERY', 'ENSAMBLE', 'Almacen', 'Cable M1', 'Cable M2']


simbols = ['/', '*', '-', '+', "'", ',', '/',
           '?', '"', '[', ']', '\\', '=', '-', '`', ';']


weight_limit = {
    'cable': 90,
    'cable batt': 400,
    'terminal': 15,
    'terminal batt': 30,
    'sello': 10,
    'tubo': 20,
    'connector': 10,
    'grommet': 10,
    'cinta': 99,
    'pret': 200
}


amount_limit = {
    'cable': 30000,
    'terminal': 20000,
    'terminal batt': 2000,
    'sello': 35000,
    'tubo': 50000,
    'connector': 1500,
    'grommet': 2300,
    'cinta': 9999,
    'pret': 9999
}

table2_headers = [
    "Yura",
    "Proveedor",
    "Cantidad",
    "Peso",
    "Maquina",
    "Area",
    "Fecha",
]

simbols = [
    "/", "*", "-", "+", "'", ",", "/",
    "?", '"', "[", "]", "\\", "=", "-",
    "`", ";",
]

# Area Styles
corte_m1 = 'QFrame { background: rgb(37, 186, 35);}'

corte_m2 = '''
    QFrame {
    background: rgb(163, 46, 231);
    }
'''
medios_m1 = '''
    QFrame {
        background: rgb(255, 160, 8);
    }
'''

medios_m2 = '''
    QFrame {
        background: rgb(66, 126, 255);
    }
'''

batt = '''
    QFrame {
        background: rgb(66, 126, 255);
    }
'''

materiales = '''
    QFrame {
        background: rgb(222, 207, 38);
    }
'''

ensamble = '''
    QFrame {
        background: rgb(255, 106, 231);
    }
'''

default = '''
    QFrame {
        background: white;
    }
'''


theme = '''
    QFrame {
        border: 1px solid black;
        border-radius: 0px;
        background-color: #000;
    }


    QPushButton{
        background-color: #fff;
        color: #000;
        border-radius: 2px;
        padding-top: 8px;
        padding-bottom: 8px;
    }

    QPushButton:hover {
        background-color: #57A2E6;
        color: #000;
        border: 2px solid #322FC5;
        border-radius: 3px;
    }

    QPushButton:disabled {
        background-color: #888888;
        color: #000;
        border-radius: 2px;
    }

    QPushButton::pressed {
        color: white;
        background-color: black;
    }

    QLabel {
        color: black;
        border-width: 0px;
        padding-left: 3px;
        padding-top: 6px;
        padding-bottom: 6px;
    }

    QLineEdit {
        background-color: #fff;
        color: black;
        border: 1px solid black;
        border-radius: 2px;
    }

    QLineEdit:hover {
        background-color: #57A2E6;
        color: #000;
        border: 2px solid #322FC5;
        border-radius: 3px;
    }

    QComboBox {
        background-color: #fff;
        border: 1px solid black;
        border-radius: 0px;
        padding-left: 4px;
        padding-top: 6px;
        padding-bottom: 6px;
        margin-left: 6px;
    }

    QComboBox QAbstractItemView {
        border: 1px solid black;
        border-radius: 0px;
        background-color: #fff;
        selection-color: #000;
        selection-background-color: #AAAAAA;
    }

    QRadioButton, QCheckBox{
        border-width: 0px;
    }

    QTableWidget {
        background-color: #fff;
        border-radius: 2px;
    }

    QHeaderView {
        border-radius: 1px;
        background-color: #fff;
    }
   '''

mat_label_theme = '''
    QLabel {
        background: white;
        color: red;
        border-style: solid;
        border-color: #000;
        border-width: 1px;
        border-radius: 2px;
    }

'''


line_theme = '''
    QLineEdit {
        background: white;
        border-style: solid;
        border-color: black;
        border-width: 1px;
        border-radius: 2px;
        padding-left: 6px;
        padding-top: 6px;
        padding-bottom: 6px;
    }

    QLineEdit:hover {
        background-color: #57A2E6;
        color: #000;
        border: 2px solid #322FC5;
        border-radius: 3px;
    }
    '''
