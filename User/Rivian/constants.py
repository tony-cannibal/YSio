
drop_columns = [0] + list(range(2,6 + 1)) + [14] + list(range(16, 20 +1)) + list(range(22, 54 + 1)) + list(range(56, 67 + 1))

drop_columns2 = [0, 4, 6, 7] + list(range(9, 29))



headers = ['Lote', 'Fecha de Orden', 'N/P', 'Rev', 'Modelo', 'Item', 'Prioridad','Hora', 'Fecha', 'Peso','Cantidad']
header_width = [90, 100, 100, 55, 60, 120, 100, 80, 100, 70, 80]


headers2 = ['Num. Reloj', 'Lote', 'Fecha de Orden','N/P', 'Rev', 'Modelo', 'Item', 'Prioridad','Hora', 'Fecha', 'Peso','Cantidad']
header_width2 = [100, 100, 90, 100, 55, 60, 120, 100, 80, 100, 70, 80]


headers3 = ['Lote', 'Area', 'Fecha de Input', 'Modelo', 'Item',
            'Prioridad', 'Numero de Parte', 'Revision', 'Cantidad de Ordenado',
            'Cantidad de Circuitos', 'Peso Ind']

simbols = [
            '/', '*', '-', '+', "'", ',' , '/', '?' , '"', '[', ']', '\\', '=', '-', '`', ';'
            ]



frame_style = '''
        QFrame {
            border-width: 1px;
            border-style: solid;
            border-color: black;
            border-radius: 0px;
            background-color: #bebebe;
            padding: 0;
            }

        QLabel {
            border-bottom: 1px solid black;
            border-top: 0px solid black;
            border-left: 0px solid black;
            border-right: 0px solid black;
            border-radius: 0px;
            }

        QLineEdit {
            border-bottom: 2px solid black;
            border-top: 0px solid black;
            border-left: 0px solid black;
            border-right: 0px solid black;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            background-color: #ffffff;
        }

        QLineEdit:hover {
            border: 2px solid blue;
            border-radius: 4px;
        }

        QTableWidget {
            alternate-background-color: #d0d0d0;
            gridline-color: #AAAAAA;
            background: #fff;
            border-radius: 0px;
        }


        QHeaderView {
           border-radius: 0px;
         }
        '''

qwidget_style = '''
    QWidget {
    }
'''


if __name__ == '__main__':
    pass
