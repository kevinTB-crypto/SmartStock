import sqlite3

def conectar():
    return sqlite3.connect('database.db', check_same_thread=False)

def crear_tablas():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            precio REAL,
            stock INTEGER,
            minimo INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            cantidad INTEGER,
            total REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    """)

    # usuario inicial
    c.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    if c.fetchone() is None:
        c.execute(
            "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
            ("admin", "1234", "Administrador")
        )

    conn.commit()
    conn.close()

        c.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            tipo TEXT,
            cantidad INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)