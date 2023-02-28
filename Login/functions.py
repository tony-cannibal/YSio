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
            # print(i)
            # print(ser_bytes.decode('ascii'))
            ser.close()
        except:
            pass
    return port


def search_user(query, database):
    try:
        con = mariadb.connect(**database)
        cur = con.cursor()
        cur.execute('SELECT * FROM empleados where noreloj = %s;',
                    (query,)
                    )
        res = cur.fetchone()
        cur.close()
        if res:
            return res
    except mariadb.OperationalError:
        res = "No Conection"
        return res


def get_inv_area(query, database):
    try:
        con = mariadb.connect(**database)
        cur = con.cursor(buffered=True)
        cur.execute('SELECT * FROM areas_inventario where codigo = %s;', (query,))
        res = cur.fetchone()
        cur.close()
        return res
    except mariadb.OperationalError:
        res = "No Conection"
        return res



if __name__ == "__main__":
    code = '42102110M111C1'
    print(type(set_port()))
