import mariadb
import pandas as pd
from datetime import date, datetime
try:
    from . import constants as cn
except ImportError:
    import constants as cn


def read_code(code):
    lot, circuit, number = code[1:-1].split(';')
    return [code, lot, circuit, number]


def check_db(query, database):
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM aduana where codigo = %s;',
                (query,))
    res = cur.fetchone()
    cur.close()
    return res


def save_circuit(info, area, database):
    today = date.today().strftime('%Y-%m-%d')
    time = datetime.now().strftime("%H:%M:%S")
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
    INSERT INTO aduana(
        codigo, lote, circuito, tabla, fecha_entrada, hora_entrada, estado, area
    ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
    ''', (info[0], info[1], info[2], info[3], today, time, cn.estados[0], area))
    con.commit()
    cur.close()


def exit_circuit(code, database):
    today = date.today().strftime('%Y-%m-%d')
    time = datetime.now().strftime("%H:%M:%S")
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
    UPDATE aduana
    SET estado = %s, fecha_salida = %s, hora_salida = %s
    WHERE codigo = %s;
    ''', (cn.estados[1], today, time, code))
    con.commit()
    con.close()


def get_enter_history(area, database):
    today = date.today().strftime('%Y-%m-%d')
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM aduana WHERE fecha_entrada = %s and area = %s;',
                (today, area))
    res = cur.fetchall()
    cur.close()
    return res


def get_exit_history(area, database):
    today = date.today().strftime('%Y-%m-%d')
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM aduana WHERE fecha_salida = %s and area = %s;',
                (today, area))
    res = cur.fetchall()
    cur.close()
    return res


def search_full_hist(query, database, area):
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM aduana
        WHERE lote = %s
        OR circuito LIKE %s
        OR codigo like %s
        AND area = %s;
        ''', ('%'+query+'%', '%'+query+'%', '%'+query+'%', area))
    res = cur.fetchall()
    cur.close()
    return res


def search_enter_date_hist(query, date_1, date_2, database, area):
    print(area)
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM aduana 
        WHERE lote = %s AND area = %s
        OR circuito LIKE %s AND area = %s
        OR codigo like %s AND area = %s
        ;
        ''', ('%'+query+'%', area, '%'+query+'%', area, '%'+query+'%', area))
    res = [i for i in cur.fetchall() if i[4] >= date_1 and i[4] <= date_2]
    # filtered_res = [ i for i in res if i[4] >= date_1 and i[4] <= date_2 ]
    cur.close()
    return res


def export_data(data, save_name):
    try:
        df = pd.DataFrame(
            data, columns=[
                'codigo', 'lote', 'circuito', 'tabla',
                'fecha de entrada', 'hora de entrada',
                'estado', 'fecha de salida',
                'hora de salida', 'area'
            ]
        )
        df['hora de entrada'] = df['hora de entrada'].values.astype(
            'datetime64')
        df['hora de salida'] = df['hora de salida'].values.astype('datetime64')
        df['hora de entrada'] = df['hora de entrada'].dt.strftime('%H:%M:%S')
        df['hora de salida'] = df['hora de salida'].dt.strftime('%H:%M:%S')
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
    query = ''

    res = search_full_hist(query, db)

    export_data(res)
