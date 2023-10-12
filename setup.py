import configparser

config = configparser.ConfigParser()
config.read(
    '//172.18.0.45/Engineering/0. Backup Ingenieria 27/Elaboracion/SIO/configuracion/sio.ini')
# config.read('src/sio.ini')


def database(use_general):
    if use_general:
        db = {
            'host': config['database']['host'],
            'database': config['database']['database'],
            'user': config['database']['user'],
            'password': config['database']['password'],
            'port': int(config['database']['port'])
        }
        return db
    else:
        db = {
            'host': '172.18.4.51',
            'database': 'yura_elaboracion',
            'user': 'yurano',
            'password': 'yuracorporation4200',
            'port': 3306
        }
        return db


if __name__ == '__main__':
    pass
