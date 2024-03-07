from data.administrador import administradorTarea
from data.basededatos import crearTabla, crearDB
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from data.administrador import administradorTarea
from data.tareas import Tarea
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from data.user import Usuario

class tareaApi(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    creada: Optional[str] = None
    actualizada: Optional[str] = None

class User(BaseModel):
    nombre: str
    apellido: str
    fechaNacimiento: str
    dni: str
    username: str
    password: str
    ultimoAcceso: Optional[str] = None
    
app = FastAPI()
crearDB('admintareas.db')
crearTabla()
administrador = administradorTarea('admintareas.db')
administrador.crearTabla()
algoritmo = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
app = FastAPI()
crypt = CryptContext(schemes=["bcrypt"])
oaouth2 = OAuth2PasswordBearer(tokenUrl="login")
Secret = "af3e251a3bdc7684f4835167aa0bfe2c80cbc9b611bf0180a078b9104ff06659"

async def autenticacion_user(token:str = Depends(oaouth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas")
    try:
        usuario = jwt.decode(token,Secret, algorithms=[algoritmo] ).get("sub")
        if usuario is None:
            raise exception
    
    except JWTError:
         raise exception
    
    user=administrador.buscarUser(usuario)
    return user[0]
    
   


async def current_user(user:User = Depends(autenticacion_user)):
        administrador = administradorTarea('admintareas.db')
        
        if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")
        return user

@app.post('/tarea')
def insertar_tarea(tarea: tareaApi):
    tarea_dict = dict(tarea)
    tarea_objeto = Tarea(**tarea_dict)
    
    
    
    if administrador.buscar_id_repetido(tarea_objeto.id):
        raise HTTPException(status_code=409, detail="Error: El ID de la tarea ya está repetido.")
    else:
        administrador.agregar_tarea(tarea_objeto)
        return tarea_objeto

@app.delete("/tarea/{id}")
def eliminar_tarea_endpoint(id: int):
    if id is None:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Se requiere un ID de tarea")

    tarea_id = administrador.eliminar_tarea(id)

    if tarea_id is not None:
        return {"mensaje": f"Tarea con ID {tarea_id} eliminada"}
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")

@app.put('/tarea/{id}/{estado}')
def actualizarestado_api(id: int, estado: str):
    tarea_actual = administrador.traer_tarea(id)
    
    if tarea_actual:
        tarea_actual.estado = estado
        tarea_actual.actualizada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        administrador.actualizar_estado_tarea(tarea_actual.id, tarea_actual.estado, tarea_actual.actualizada)
        return {"mensaje": f"Tarea con id {id} actualizada"}
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")

@app.get('/tarea/{id}')
def traertarea_api(id: int):
    tarea = administrador.traer_tarea(id)
    
    if tarea:
        return tarea
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea con ese id")

@app.post("/user")
async def agregar_user(user: User):
    administrador = administradorTarea('admintareas.db')
    
    # Verificar si el usuario ya existe en la base de datos
    if administrador.buscarUser(user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe en la base de datos")
    
    administrador.agregarUser(user)
    usuario = administrador.buscarUser(user.username)
    return {"mensaje": f"Usuario: {usuario[0]} agregado"}

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    administrador = administradorTarea('admintareas.db')
    username = form.username

    usuario = administrador.buscarUser(username)  # Asegúrate de pasar el argumento 'username'
    

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
# Verifica si la contraseña esta verificada
   

    if not crypt.verify(form.password, usuario[1]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    

    # Actualiza el último acceso del usuario con la hora actual
    ultimo_acceso_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    datos_usuario = administrador.buscar_datos_usuario(username)
    user = Usuario(*datos_usuario)
    
    user.actualizar_ultimo_acceso(ultimo_acceso_actual)


    access_token = {"sub": usuario[0], 
                    "exp": datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)}
    
    return {"access_token": jwt.encode(access_token, Secret, algorithm=algoritmo), 
            "token_type": "bearer",
            }



@app.get("/user/me")
async def me(user:User = Depends(current_user)):
    return user

