import pymysql

def init_sql(user,password,db):
    conn = pymysql.connect(host='localhost',user=user,password=password,db=db,charset='utf8')
    return conn

def initialize(user,password):
    conn = pymysql.connect(host='localhost',user=user,password=password,charset='utf8')
    create_db(conn)
    conn = pymysql.connect(host='localhost',user=user,password=password,db='hackerton',charset='utf8')
    create_user_table(conn)
    create_address_table(conn)
    create_visit_table(conn)
    create_diary_table(conn)
    create_store_tbl(conn)
    conn.commit()

def create_db(conn):
    cursor = conn.cursor()
    create_db_sql='create database hackerton'
    cursor.execute(create_db_sql)

def create_user_table(conn):
    cursor = conn.cursor()
    create_address_table_sql = '''CREATE TABLE user_tbl (
        user_id VARCHAR(30) PRIMARY KEY,
        user_name VARCHAR(30)
    ) CHARSET=utf8;'''
    cursor.execute(create_address_table_sql)
    print("create_user_table complete")

def create_address_table(conn):
    cursor = conn.cursor()
    create_address_table_sql = '''CREATE TABLE address_tbl (
        map_id VARCHAR(30) PRIMARY KEY,
        addr VARCHAR(100) NOT NULL,
        longtitude FLOAT NOT NULL,
        latitude FLOAT NOT NULL
    ) CHARSET=utf8;'''
    cursor.execute(create_address_table_sql)
    print("create_address_table complete")

def create_visit_table(conn):
    cursor = conn.cursor()
    create_address_table_sql = '''CREATE TABLE visit_tbl (
        visit_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(30) NOT NULL,
        map_id VARCHAR(30) NOT NULL,
        addr VARCHAR(100) NOT NULL,
        store_name VARCHAR(100),
        start_datetime datetime,
        end_datetime datetime,
        is_diary BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES user_tbl(user_id) ON UPDATE CASCADE,
        FOREIGN KEY (map_id) REFERENCES address_tbl(map_id) ON UPDATE CASCADE
    ) CHARSET=utf8;'''
    cursor.execute(create_address_table_sql)
    print("create_visit_table complete")

def create_diary_table(conn):
    cursor = conn.cursor()
    create_address_table_sql = '''CREATE TABLE diary_tbl (
        diary_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(30) NOT NULL,
        visit_id INT NOT NULL,
        content VARCHAR(1000),
        photo VARCHAR(100),
        visible BOOLEAN DEFAULT false,
        FOREIGN KEY (user_id) REFERENCES user_tbl(user_id) ON UPDATE CASCADE,
        FOREIGN KEY (visit_id) REFERENCES visit_tbl(visit_id) ON UPDATE CASCADE
    ) CHARSET=utf8;'''
    cursor.execute(create_address_table_sql)
    print("create_diary_table complete")

def create_store_tbl(conn):
    cursor = conn.cursor()
    create_address_table_sql = '''CREATE TABLE store_tbl (
        store_id INT AUTO_INCREMENT PRIMARY KEY,
        map_id VARCHAR(30) NOT NULL,
        store_name VARCHAR(100),
        category VARCHAR(100),
        img VARCHAR(200),
        dong VARCHAR(30),
        longtitude FLOAT NOT NULL,
        latitude FLOAT NOT NULL
        FOREIGN KEY (map_id) REFERENCES address_tbl(map_id) ON UPDATE CASCADE
    ) CHARSET=utf8;'''
    cursor.execute(create_address_table_sql)
    print("create_store_table complete")

    
if __name__ == '__main__':
    id = input("mysql id : ")
    pw = input('mysql pw : ')
    initialize(id,pw)

