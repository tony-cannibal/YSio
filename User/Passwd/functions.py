
import mariadb

def update_password(noreloj, newpass, database):
    con = mariadb.connect(**database)
    cur = con.cursor()
    cur.execute('''
    UPDATE empleados
    SET passwd = %s
    WHERE noreloj = %s;
    ''', (newpass, noreloj))
    con.commit()
    cur.close()
    con.close()



if __name__ == '__main__':
    pass
    # db = {
    #     "host": "172.18.4.58",
    #     "database": "yura_elaboracion",
    #     "user": "yura_admin",
    #     "password": "Metallica24+",
    #     "port": 3306
    #     }
    # noreloj = 17040267
    # newpass = 17040267
    # update_password(noreloj, newpass, db)
