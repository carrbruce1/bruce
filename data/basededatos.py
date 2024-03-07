import sqlite3 as sql
from data.tareas import Tarea


def crearDB(db_file):
    conn = sql.connect(db_file)
    conn.commit()
    conn.close()

def crearTabla():
    conn = sql.connect('admintareas.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            creada TEXT,
            actualizada TEXT 
    )""")
    conn.commit()
    conn.close()

