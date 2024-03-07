from data.tareas import Tarea
import sqlite3 as sql
from fastapi import HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
import random


class User(BaseModel):
    username: str
    password: str
    ultimoAcesso: str | None

crypt = CryptContext(schemes=["bcrypt"])

class administradorTarea:
    def __init__(self, db_file:str):
        self.db = sql.connect(db_file)

        
    def agregar_tarea(self, tarea: Tarea) -> int:
        tarea_dic = tarea.tarea_dict()
            
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO tareas (id, titulo, descripcion, estado, creada, actualizada)
                        VALUES (?, ?, ?, ?, ?, ?)""", tuple(tarea_dic.values()))
        tarea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return tarea_id
    
    def buscar_id_repetido(self, id):
    # Conectar a la base de datos
        conexion = sql.connect('admintareas.db')
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para buscar el campo "id" repetido
        
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE id = ?", (id,))

        # Obtener el resultado
        resultado = cursor.fetchone()
        
        ids = resultado[0]
        
        # Cerrar la conexión a la base de datos
        conexion.close()
        
        # Verificar si el ID está repetido
        
        return ids

    def traer_tarea(self, tarea_id: int) -> Tarea:
       
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id=?"
        ,(tarea_id,))
        tarea = cursor.fetchone()
        conn.commit()
        conn.close()

        
        if tarea:
            # print(tarea)
            return Tarea(*tarea)
        else:
            return None

    def traer_todas_tareas(self):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas"
        )
        tareas = cursor.fetchall()
        conn.commit()
        conn.close()
        return tareas
    
    def eliminar_tarea(self, tarea_id: int):
        if tarea_id is None:
            raise ValueError("El ID de la tarea no puede ser nulo")

        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()

        # Consultar la tarea antes de eliminarla
        cursor.execute("SELECT id FROM tareas WHERE id=?", (tarea_id,))
        tarea = cursor.fetchone()

        if tarea:
            # Guardar el ID de la tarea eliminada
            tarea_eliminada_id = tarea[0]

            # Eliminar la tarea
            cursor.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))
            conn.commit()

            conn.close()
            return tarea_eliminada_id
        else:
            conn.close()
            raise HTTPException(status_code=404, detail="No se encontró la tarea")
        
    def actualizar_estado_tarea(self, tarea_id: int, estado: str, actualizada:str):
       
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado=?, actualizada=? WHERE id=?", (estado, actualizada, tarea_id))
        conn.commit()
        conn.close()

    def crearTabla(self):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                    nombre TEXT,
                    apellido TEXT,
                    fechaNacimiento DATE,
                    dni TEXT,
                    user TEXT,
                    password TEXT,
                    ultimoAcceso TEXT
                    )""")
        conn.commit()
        conn.close()

    def agregarUser(self, user: User):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        hashed_password = crypt.hash(user.password)
        cursor.execute("""INSERT INTO usuarios (nombre, apellido , fechaNacimiento, dni, user, password)
                        VALUES (?,?,?,?,?,?)""", (user.nombre,user.apellido,user.fechaNacimiento,user.dni,user.username, hashed_password))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def actualizar_ultimo_acceso(self, username: str, ultimo_acceso: str):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()

        # Actualiza el campo "ultimoAcceso" del usuario con el valor proporcionado.
        cursor.execute("UPDATE usuarios SET ultimoAcceso=? WHERE user=?", (ultimo_acceso, username))
        conn.commit()
        conn.close()

    
    def buscarUser(self, username: str) -> tuple:
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user, password, ultimoAcceso FROM usuarios WHERE user=?", (username,))
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            return resultado  # Devuelve una tupla con el usuario, contraseña y último acceso
        else:
            return None
    
    def buscar_datos_usuario(self, username: str):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()

        cursor.execute("SELECT password, ultimoAcceso, user,nombre, apellido, fechaNacimiento, dni FROM usuarios WHERE user=?", (username,))
        resultado = cursor.fetchone()

        conn.close()

        return resultado
    
    def eliminarUser(self, username: User):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE user=?", (username,))
        conn.commit()
        conn.close()


    def generar_numero_aleatorio(self) -> int:
        numero_aleatorio = random.randint(1, 1000)
        return numero_aleatorio
