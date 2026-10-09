import sqlite3

def create_database():
    conn = sqlite3.connect(database=r'ims_database.db')
    cursor = conn.cursor()

     #======Create Employee table========
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
         eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text
       )
    ''')
    conn.commit()
    #======Create Supplier table========
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS supplier (
         invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,description text
       )
    ''')
    conn.commit()
    #======Create Category table========
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
         cat_id INTEGER PRIMARY KEY AUTOINCREMENT,name text
       )
    ''')
    conn.commit()
    #======Create Product table========
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
         pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,price text,qty text,status text
       )
    ''')
    conn.commit()

create_database()