import configparser

localConf = "/src/sio.ini"
# remoteConf = "//172.18.0.45/Engineering/0. Backup Ingenieria 27/Elaboracion/SIO/configuracion/sio.ini"
remoteConf = "//172.18.4.8/Ingeniería/Engineering Server/Luis/SIO/CONFIGURACION/sio.ini"


def database(use_general, rootPath):
    config = configparser.ConfigParser()
    # if use_general:
    try:
        config.read(remoteConf)
        db = {
            "host": config["database"]["host"],
            "database": config["database"]["database"],
            "user": config["database"]["user"],
            "password": config["database"]["password"],
            "port": int(config["database"]["port"]),
        }
        return db
    # else:
    except:
        config.read(rootPath + localConf)

        db = {
            "host": config["database"]["host"],
            "database": config["database"]["database"],
            "user": config["database"]["user"],
            "password": config["database"]["password"],
            "port": int(config["database"]["port"]),
        }

        # db = {
        #     "host": "172.18.4.58",
        #     "database": "yura_elaboracion",
        #     "user": "yura_admin",
        #     "password": "Metallica24+",
        #     "port": 3306,
        # }

        return db


if __name__ == "__main__":
    pass
