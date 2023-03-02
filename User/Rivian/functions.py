import mariadb
import pandas as pd
import serial
import serial.tools.list_ports
from datetime import date, datetime, time, timedelta
try:
    from . import constants as cn
except ImportError:
    import constants as cn


def get_lot(code:str)->list:
    lot = code[1:11]
    return lot

def set_port():
    ports = []
    for i in serial.tools.list_ports.comports():
        ports.append(i[0])
    port = ''
    for i in ports:
        try:
            ser = serial.Serial(
                port=i,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1,
                write_timeout=1
            )
            ser.write('P'.encode('ascii'))
            ser_bytes = ser.read(8)
            if ser_bytes:
                port = i
            ser.close()
        except:
            pass
    return port

def lot_search(lot, db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute('SELECT * FROM input_riv where lote = %s;', (lot,))
    res = cur.fetchone()
    cur.close()
    return res


def get_riv_part(database: dict)->dict:
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM rivian_part;')
    res = cur.fetchall()
    cur.close()
    part_num = {}
    for i in res:
        part_num[i[0]] = i
    return part_num

def get_database_input(db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute('SELECT * FROM input_riv;')
    res = cur.fetchall()
    cur.close()
    lots = [ i[0] for i in res ]
    return lots

def get_riv_lots(database:dict)->list:
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM rivian_inv')
    res = cur.fetchall()
    lots = [i[1] for i in res]
    return lots

def get_riv_inv(database, date):
    con = mariadb.connect(**database)
    date = datetime(year=date[0], month=date[1], day=date[2])
    cur = con.cursor()
    query = f"SELECT * FROM rivian_inv WHERE fecha_entrada = '{date}';"
    cur.execute(query)
    res = cur.fetchall()
    # for i in res:
    #     i[6] = i[6].strftime("%Y-%m-%d")
    return res

def save_input(carga, db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    # for i in carga:
    cur.execute('''
    INSERT INTO input_riv(
    lote, area, fecha_de_input, modelo,
    item, prioridad, num_parte,
    rev, cant_ordenado, cant_circuitos, peso_ind
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    );''', (carga[0], carga[1], carga[2], carga[3], carga[4],
            carga[5], carga[6], carga[7], carga[8], carga[9], carga[10]))
    con.commit()
    cur.close()

def upload_record(record, database):
    con = mariadb.connect(**database)
    cur = con.cursor()

    cur.execute('''
    INSERT INTO rivian_inv(noreloj, lote, fecha_de_input, numero_parte, rev,
    modelo, item, prioridad, hora_entrada, fecha_entrada, peso, catidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    ''',(record[0], record[1], record[2], record[3], record[4],
    record[5], record[6], record[7], record[8], record[9], record[10], record[11]))

    con.commit()
    cur.close()

def inv_search(query, database):
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM rivian_inv WHERE lote LIKE %s;', ('%'+query+'%',))
    res = cur.fetchall()
    cur.close()
    res = [ list(i) for i in res ]
    return res

def read_weight(puerto):
    ser = serial.Serial(
        port=puerto,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
        write_timeout=1
    )
    ser.write('P'.encode('ascii'))
    weight = ser.read(8).decode('ascii').strip()
    return weight

def get_riv_input(file: str, part: dict) -> list:
    carga = pd.read_excel(file.upper())
    carga = carga.drop(carga.columns[cn.drop_columns], axis=1)
    carga_list = carga.values.tolist()
    for i in carga_list:
        i[2] = i[2].to_pydatetime().strftime('%Y-%m-%d')
        if len(str(i[8])) == 1:
            i[8] = '0' + str(i[8])
    riv = []
    for i in carga_list:
        if i[7] in part and part[i[7]][-1] != 'A':
            riv.append(i)
    for i in riv:
        i[0] = str(i[0])
        i[5] = part[i[7]][3]
        i.append(part[i[7]][-2])
    return riv

def get_riv_input_2(file, part):
    carga =  pd.read_excel(file)
    carga = carga.drop(carga.columns[cn.drop_columns2], axis=1)
    carga['np'] = carga['P/N'].str[:-3]
    carga['rev'] = carga['P/N'].str[-2:]
    carga_list = carga.values.tolist()
    carga_list.pop()
    riv = [i for i in carga_list if i[5] in part and part[i[5]][-1] != 'A']
    for i in riv:
        i[0] = i[0].to_pydatetime().strftime('%Y-%m-%d')
        i[1] = str(int(i[1]))
        i[4] = str(int(i[4]))
        i.append(part[i[5]][2])
        i.append(part[i[5]][3])
        i.append(part[i[5]][4])
        i.append(part[i[5]][5])
        i.append(part[i[5]][1])
    myorder = [4, 11, 0, 7, 8, 1, 5, 6, 3, 9, 10]
    res = []
    for i in riv:
        res.append([ i[n] for n in myorder ])
    return res

def export_data(data, save_name):
    try:
        df = pd.DataFrame(
            data, columns=[
                'Numero de Reloj', 'Lote', 'Fecha de Orden','N/P', 'Rev',
                'Modelo', 'Item', 'Prioridad','Hora de Entrada',
                'Fecha de Entrada', 'Peso', 'Cantidad'
            ]
        )
        df['Hora de Entrada'] = df['Hora de Entrada'].values.astype('datetime64')
        df['Hora de Entrada'] = df['Hora de Entrada'].dt.strftime('%H:%M:%S')
        df.to_excel(save_name, index=False)
    except ValueError:
        pass



if __name__ == '__main__':

    db = {
        "host": "172.18.4.58",
        "database": "yura_elaboracion",
        "user": "yura_admin",
        "password": "Metallica24+",
        "port": 3306
        }
    part = get_riv_part(db)
    file = '2023-01-26.xlsx'

    result = get_riv_input_2(file, part)
    for i in range(11):
        print(i)

