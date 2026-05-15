import sqlite3

def conectar():
    return sqlite3.connect('database.db', check_same_thread=False)

def crear_tablas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria TEXT,
        precio REAL,
        stock INTEGER,
        minimo INTEGER
    )
    ''')
    conn.commit()
    conn.close()