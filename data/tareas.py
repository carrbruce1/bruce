import datetime
from typing import Optional
class Tarea:
    
    def __init__(self, id: int, titulo:str, descripcion: str, estado:  str, creada: Optional[str] = None, actualizada: Optional[str] = None):
    
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        if creada is None:
            self.creada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else: 
            self.creada = creada
        self.actualizada = actualizada


    def tarea_dict(self)-> dict:
        return {
            "id" : self.id,
            "titulo" : self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "creada": self.creada,
            "actualizada": self.actualizada
        } 
    
    def obtener_id(self) -> id:
        return self.id
    
    def __str__(self):
        return f"Tarea: ID={self.id}, Título={self.titulo}, Descripción={self.descripcion}, Estado={self.estado}, Creada={self.creada}, Actualizada={self.actualizada}"