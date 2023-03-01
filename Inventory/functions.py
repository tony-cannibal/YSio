import mariadb
import serial
import serial.tools.list_ports

try:
    from . import constants as cn
except ImportError:
    import constants as cn


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

def calc_amount(tipo:str, weight:float, ind_weight:float, tara:int, use_pkg=True)->int:
        if not use_pkg:
            tara = 0
        if tipo.lower() == "sello":
            return round((weight * 1000) / ind_weight, 1)
        else:
            try:
                return round((weight - tara) / ind_weight, 1)
            except ZeroDivisionError:
                return 0


def get_machines(area:str, sub_area:str, database:dict)->list:
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM maquinas
        where area = %s and sub_area = %s ;
        ''', (area, sub_area)
                )
    res = cur.fetchall()
    cur.close()
    return res

def capture_value(item:list, equipo:str, sub_area:str,database:dict):
    # print(item)
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
    INSERT INTO inventario_mensual(
        proveedor, yura, tipo, cantidad, peso, valor, maquina,
        equipo, area, sub_area, fecha
        )
    VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
    ''', (item[0], item[1], item[2], item[3], item[5],
          item[8], item[4], equipo, item[6], sub_area, 
          item[7]))
    con.commit()
    # print('this should commit')
    cur.close()

def read_weight(puerto):
    ser = serial.Serial(
        port=puerto,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
        write_timeout=1)
    ser.write('P'.encode('ascii'))
    weight = ser.read(8).decode('ascii').strip()
    return weight

def search_mats(data:dict, query:str)-> list:
    query = query.upper()
    q = query.find('Q')
    res = []
    for i in data.values():

        if len(query) >= 20:
            if query[1:q] in i[0]:
                res.append(i)
        else:
            if query in i[0]:
                res.append(i)
    return res

def get_materiales(database:dict)-> list:
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM materiales;')
    res = cur.fetchall()
    cur.close()
    res = [list(i) for i in res]

    for i in res:
        i[0] = f'{i[1]} {i[2]} {i[3]}'
    return res

def get_materiales_cables(database:dict)-> list:
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute("SELECT * FROM materiales where tipo = 'CABLE';")
    res = cur.fetchall()
    cur.close()
    res = [list(i) for i in res]
    for i in res:
        i[0] = f'{i[1]} {i[2]} {i[3]}'
    return res


if __name__ == "__main__":
    mats = get_materiales()
    materials = {}
    query = 'PB1F1PK0Q1800SO122914100'.upper()
    for i in mats:
        materials[i[2]] = i

    res = search_mats(materials, query)
    for i in res:
        print(i)
