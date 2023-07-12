import mariadb
import serial
import serial.tools.list_ports
from datetime import date

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
        except BaseException:
            pass
    return port


def set_style(name):
    if name == cn.areas[0] or name == cn.areas[7]:
        return cn.corte_m1
    elif name == cn.areas[1]:
        return cn.medios_m1
    elif name == cn.areas[2] or name == cn.areas[8]:
        return cn.corte_m2
    elif name == cn.areas[3]:
        return cn.medios_m2
    elif name == cn.areas[4]:
        return cn.batt
    elif name == cn.areas[6]:
        return cn.materiales
    elif name == cn.areas[5]:
        return cn.ensamble
    else:
        return cn.default


def calc_amount(
        tipo: str,
        weight: float,
        ind_weight: float,
        tara: int,
        use_pkg=True) -> int:
    if not use_pkg:
        tara = 0
    if tipo.lower() == "sello":
        return round((weight * 1000) / ind_weight, 1)
    else:
        try:
            return round((weight - tara) / ind_weight, 1)
        except ZeroDivisionError:
            return 0


def get_machines(area: str, sub_area: str, database: dict) -> list:
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


def capture_value(item: list, equipo: str, sub_area: str, database: dict):
    # print(item)
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
    INSERT INTO inventario_mensual(
        proveedor, yura, tipo, cantidad, peso, valor, maquina,
        equipo, area, sub_area, codigo
        )
    VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
    ''', (item[0], item[1], item[2], item[3], item[5],
          item[7], item[4], equipo, item[6], sub_area,
          item[8]))
    con.commit()
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


def search_mats(data: dict, query: str) -> list:
    query = query.upper()
    q = query.find('Q')
    res = []
    for i in data.values():

        if len(query) >= 20:
            if query in i[0]:
                res.append(i)
        else:
            if query in i[0]:
                res.append(i)
    return res


def get_materiales(database: dict) -> list:
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('SELECT * FROM materiales;')
    res = cur.fetchall()
    cur.close()
    res = [list(i) for i in res]

    for i in res:
        i[0] = f'{i[1]} {i[2]} {i[3]}'
    return res


def get_materiales_cables(database: dict) -> list:
    con = mariadb.connect(**database)
    cur = con.cursor()
    # cur.execute(
    #     "SELECT * FROM materiales where tipo = 'CABLE';")
    cur.execute(
        "SELECT * FROM materiales where tipo = 'CABLE' OR tipo = 'CABLE SAM';")
    res = cur.fetchall()
    cur.close()
    res = [list(i) for i in res]
    for i in res:
        i[0] = f'{i[1]} {i[2]} {i[3]}'
    return res


def check_master(equipo):
    if equipo == 'Master':
        return True
    else:
        return False


def check_service(equipo):
    if equipo == 'Service':
        return True
    else:
        return False


def check_cable(cable: str) -> bool:
    if cable.lower() == 'cable':
        return True
    else:
        return False


def get_qty(code: str, qcount: int) -> str:
    start = 0
    end = 0
    if qcount == 2:
        start = code.rfind('Q') + 1
    else:
        start = code.find('Q') + 1
    end = code.find('S', start)
    return code[start:end]


def get_subcode(code: str, qcount: int) -> str:
    if code[-1] == "Q":
        code = code[:-2]
    start = 1
    end = 0
    if qcount == 2:
        end = code.rfind('Q')
    else:
        end = code.find('Q')
    return code[start:end]


def check_code(code_text: str):
    if code_text[-1] == "Q":
        code_text = code_text[:-2]
    code_elements = {}
    code_elements["P"] = code_text[0] if code_text != '' else ''


def get_code_elements(code: str) -> list:
    if len(code) >= 22:
        qcount = code.count('Q')
        qty = get_qty(code, qcount)
        subcode = get_subcode(code, qcount)
        elements = [code, subcode, qty]
        return elements
    else:
        elements = [code, code, '']
        return elements


def check_pkg(current, code_elements):
    try:
        if current[1] == code_elements[1]:
            current[7] = code_elements[2]
        return current
    except IndexError:
        return []


def manual_input(database, master):
    if master:
        return True
    else:
        con = mariadb.connect(**database)
        cur = con.cursor()
        cur.execute("SELECT * FROM conditions WHERE state = 'manual input';")
        res = cur.fetchall()
        cur.close()
        if res[0][2] == 1:
            return True
        else:
            return False


def get_history(maquina: str, equipo: str, db: dict):
    fecha = date.today().strftime("%Y-%m-%d") + '%'  # Fecha
    # print(maquina, equipo, fecha)
    con = mariadb.connect(**db)
    cur = con.cursor()

    cur.execute("SELECT * FROM conditions WHERE state = 'check history';")
    history_condition = cur.fetchone()[2]
    if history_condition == 1:
        cur.execute('''
            SELECT * FROM inventario_mensual WHERE maquina = %s
                    AND fecha LIKE %s;
                    ''', (maquina, fecha))
        res = cur.fetchall()
        history = []
        for i in res:
            # print(i)
            history.append(list(i))
        # print(history)
        return history
    else:
        return []


if __name__ == "__main__":
    mats = get_materiales()
    materials = {}
    query = 'PB1F1PK0Q1800SO122914100'.upper()
    for i in mats:
        materials[i[2]] = i

    res = search_mats(materials, query)
    for i in res:
        print(i)
