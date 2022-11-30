import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Creates a connection to the database. """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_location(conn, loc):
    """Adds the information gathered from the API and adds to the database to the
    Param: 
        conn = connection to the database
        loc = The location to be greated"""
    try:
        sql = ''' INSERT OR IGNORE INTO locations(location,lat,lon,alt,address)
                VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, loc)
        conn.commit()
    except:
        x = 0
    return cur.lastrowid


def check_if_exists(conn,loc,dataadd):
    cur = conn.cursor()
    cur.execute(f"SELECT rowid FROM locations WHERE location = ?" ,(loc,)) 
    data=cur.fetchall()
    if len(data)==0:
        create_location(conn, dataadd)
        print('There is no component named %s'%loc)
    else:
        print('Component %s found with rowids %s'%(loc,','.join(map(str, next(zip(*data))))))

def check_if_location_exists(conn,loc,dataadd):
    cur = conn.cursor()
    cur.execute(f"SELECT rowid FROM locations WHERE location = ?" ,(loc,)) 
    data=cur.fetchall()
    if len(data)==0:
        create_location(conn, dataadd)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM locations WHERE location = ?", (loc,))
        sqlresult = cur.fetchall()
        return  sqlresult
    else:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM locations WHERE location = ?", (loc,))
        sqlresult = cur.fetchall()
        return  sqlresult

def fetch_location_information(conn,loc):
    cur = conn.cursor()
    #sql = cur.execute(f"SELECT rowid FROM locations WHERE location = {loc}")
    cur.execute(f"SELECT * FROM locations WHERE location = ?", (loc,))
    sqlresult = cur.fetchall()
    return sqlresult

def main(data):
    database = r"./db/locationData.db"

    # creates a database connection
    conn = create_connection(database)
    with conn:
        check_if_location_exists(conn,data[0],data)
    
if __name__ == '__main__':
    
    main()