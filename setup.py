import configparser

config = configparser.ConfigParser()
config.read('//172.18.0.45/Engineering/0. Backup Ingenieria 27/Elaboracion/SIO/configuracion/sio.ini')
# config.read('src/sio.ini')

db = {
    'host': config['database']['host'],
    'database': config['database']['database'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'port': int(config['database']['port'])
}





if __name__ == '__main__':
    pass
