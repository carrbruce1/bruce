import sqlite3 as sql

class Persona:
    def __init__(self, nombre, apellido, fechaNacimiento, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.fechaNacimiento = fechaNacimiento
        self.dni = dni


class Usuario(Persona):
    def __init__(self, contraseña, ultimoAcceso,usuario, nombre, apellido, fechaNacimiento, dni):
        super().__init__(nombre, apellido, fechaNacimiento, dni)
        self.contra = contraseña
        self.ultimoAcesso = ultimoAcceso
        self.user = usuario
    
    def actualizar_ultimo_acceso(self, nuevo_ultimo_acceso: str):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        # Actualizar el campo "ultimoAcceso" del usuario con el valor proporcionado.
        cursor.execute("UPDATE usuarios SET ultimoAcceso=? WHERE user=?", (nuevo_ultimo_acceso, self.user))
        conn.commit()
        conn.close()

    def obtener_ultimo_acceso(self):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ultimoAcceso FROM usuarios WHERE user=?", (self.user,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]  # Devuelve el último acceso como un valor de tipo str
        else:
            return None
    
    
       
        