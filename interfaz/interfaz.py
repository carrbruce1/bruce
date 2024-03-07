import tkinter as tk
from tkinter import messagebox
import requests
import json
from data.administrador import administradorTarea
from data.user import Usuario

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana principal")
        ancho = self.winfo_screenwidth()
        altura = self.winfo_screenheight()
        self.geometry("350x400")
        self.config(bg='#e2d0bc')
        self.ventana_principal = self
        self.token_ingresado = None
        self.ventana_tareas = None 
        self.label_usuario = None
        
        btn_iniciar_sesion = tk.Button(self, text="Iniciar sesión", command=self.login, width=15)
        btn_iniciar_sesion.pack(pady=10)
        btn_registrarse = tk.Button(self, text="Registrarse", command=self.abrir_ventana_registro, width= 15)
        btn_registrarse.pack(pady=10)

       
    def abrir_ventana_registro(self):
        ventana_registro = tk.Toplevel(self)
        ventana_registro.title('Registrarse')
        ventana_registro.geometry("300x300")

        nombre_label = tk.Label(ventana_registro, text="Nombre:")
        nombre_label.pack()

        nombre_entry = tk.Entry(ventana_registro, width=30)
        nombre_entry.pack()

        apellido_label = tk.Label(ventana_registro, text="Apellido:")
        apellido_label.pack()

        apellido_entry = tk.Entry(ventana_registro, width=30)
        apellido_entry.pack()

        fecha_label = tk.Label(ventana_registro, text="Fecha de nacimiento:")
        fecha_label.pack()

        fecha_entry = tk.Entry(ventana_registro, width=30)
        fecha_entry.pack()

        dni_label = tk.Label(ventana_registro, text="Dni:")
        dni_label.pack()

        dni_entry = tk.Entry(ventana_registro, width=30)
        dni_entry.pack()

        usuario_label = tk.Label(ventana_registro, text="Usuario:")
        usuario_label.pack()

        usuario_entry = tk.Entry(ventana_registro, width=30)
        usuario_entry.pack()

        contraseña_label = tk.Label(ventana_registro, text="Contraseña:")
        contraseña_label.pack()

        contraseña_entry = tk.Entry(ventana_registro, width=30)
        contraseña_entry.pack()

        def do_registro():
            nombre = nombre_entry.get()
            apellido = usuario_entry.get()
            fechaNacimiento = fecha_entry.get()
            dni = dni_entry.get()
            usuario = usuario_entry.get()
            contraseña = contraseña_entry.get()

            data = {
                "nombre": nombre,
                "apellido":apellido,
                "fechaNacimiento":fechaNacimiento,
                "dni": dni,
                "username": usuario,
                "password": contraseña,
                "ultimoAcceso": ""
            }
            
            print("Enviando datos de registro:", data)

            response = requests.post('http://127.0.0.1:8000/user', json=data)

            print("Respuesta del servidor:", response.status_code, response.json())

            if response.status_code == 200:
                messagebox.showinfo("Usuario registrado", "El usuario ha sido registrado exitosamente.")
                ventana_registro.destroy()
            elif response.status_code == 409:
                mensaje_error = response.json().get("detail", "Ocurrió un error al registrar el usuario.")
                messagebox.showerror("Error", mensaje_error)

        btn_registrar = tk.Button(ventana_registro, text="Enviar", command=do_registro)
        btn_registrar.pack(pady=10)


    def login(self):
        ventana = tk.Toplevel()
        ventana.title('Iniciar sesión')
        ancho = ventana.winfo_screenwidth()
        altura = ventana.winfo_screenheight()
        ventana.geometry(f"{300}x{400}")

        username_label = tk.Label(ventana, text="Usuario:")
        username_label.pack()

        username_entry = tk.Entry(ventana)
        username_entry.pack()

        password_label = tk.Label(ventana, text="Contraseña:")
        password_label.pack()

        password_entry = tk.Entry(ventana, show="*")
        password_entry.pack()


   
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            # Realizar el login utilizando las credenciales
            data = {
                "username": username,
                "password": password
            }
            response = requests.post('http://127.0.0.1:8000/login', data=data)
            if response.status_code == 200:
                access_token = response.json()["access_token"]
                ventana_token = tk.Toplevel()
                ventana_token.title("Token de acceso")
                ancho = ventana_token.winfo_screenwidth()
                altura = ventana_token.winfo_screenheight()
                ventana_token.geometry(f"{ancho}x{altura}")

                text_widget = tk.Text(ventana_token)
                text_widget.insert(tk.END, access_token)
                text_widget.pack(fill=tk.BOTH, expand=True)
                self.token_ingresado = access_token
               
                btn_enviar = tk.Button(ventana_token, text="Enviar", command=lambda: enviar_token(access_token))
                btn_enviar.pack(pady=10)
            else:
                mensaje_error = response.json().get("detail", "Inicio de sesión fallido. Usuario o contraseña incorrectos.")
                messagebox.showerror("Error", mensaje_error)

           
        btn_login = tk.Button(ventana, text="Iniciar sesión", command=do_login)
        btn_login.pack(pady=10)
    
        def enviar_token(token):
            def do_enviar():
                token_ingresado = token_entry.get()
                # Aquí puedes realizar la lógica para enviar el token al servidor
                headers = {
                    "Authorization": f"Bearer {token_ingresado}"
                }
                response = requests.get('http://127.0.0.1:8000/user/me', headers=headers)
                if response.status_code == 200:
                    user = response.json()
                    # Realizar acciones con la respuesta del servidor
                    messagebox.showinfo("Token válido", "El token es válido. Usuario: {}".format(user))
                    ventana_enviar.destroy()
                    self.open_ventana_tareas(token_ingresado)
                else:
                    messagebox.showerror("Error", "El token es inválido o ha expirado.")

            ventana_enviar = tk.Toplevel()
            ventana_enviar.title("Enviar token")
            ancho = ventana_enviar.winfo_screenwidth()
            altura = ventana_enviar.winfo_screenheight()
            ventana_enviar.geometry(f"{300}x{400}")
            token_label = tk.Label(ventana_enviar, text="Token de acceso:")
            token_label.pack()

            token_entry = tk.Entry(ventana_enviar, width=300)
            token_entry.pack()

            # Agregar botón para enviar el token
            btn_enviar = tk.Button(ventana_enviar, text="Enviar", command=do_enviar)
            btn_enviar.pack(pady=10)

            
            ventana.destroy()

    
    def open_ventana_tareas(self, token_ingresado):
        if(token_ingresado):    
            if self.ventana_tareas is None or not self.ventana_tareas.winfo_exists():
                # Si la ventana de tareas no existe o ha sido cerrada,
                # crear una nueva instancia y almacenarla en el atributo
                self.ventana_tareas = tk.Toplevel(self)
                self.ventana_tareas.title("Ventana de tareas")
                ancho = self.ventana_tareas.winfo_screenwidth()
                altura = self.ventana_tareas.winfo_screenheight()
                self.ventana_tareas.geometry(f"{ancho}x{altura}")
                self.ventana_tareas.config(bg="lightblue")

                
                
                    
                btn_usuario = tk.Button(self.ventana_tareas, text="Usuario", command=self.mostrar_usuario, width=15)
                btn_usuario.pack(pady=10)
                

                btn_crear_tarea = tk.Button(self.ventana_tareas, text="Crear tarea", command=self.crear_tarea, width=15)
                btn_crear_tarea.pack(pady=10)

                btn_traer_tarea = tk.Button(self.ventana_tareas, text="Traer tarea", command=self.traer_tarea, width=15)
                btn_traer_tarea.pack(pady=10)

                btn_actualizar_estado = tk.Button(self.ventana_tareas, text="Actualizar estado", command=self.actualizar_estado, width=15)
                btn_actualizar_estado.pack(pady=10)

                btn_eliminar_tarea = tk.Button(self.ventana_tareas, text="Eliminar tarea", command=self.eliminar_tarea, width=15)
                btn_eliminar_tarea.pack(pady=10)
        else:
            self.login()

  


    def mostrar_usuario(self):
        headers = {"Authorization": f"Bearer {self.token_ingresado}"}
        response = requests.get('http://127.0.0.1:8000/user/me', headers=headers)
        administrador = administradorTarea('admintareas.db')
        
        if response.status_code == 200:
            try:

                user_data = response.json()
                
                usuario = administrador.buscarUser(user_data)
                datos_usuario = administrador.buscar_datos_usuario(user_data)
                user = Usuario(*datos_usuario)
                ultimo_acceso = user.obtener_ultimo_acceso()
                if usuario:
                    ventana = tk.Tk()  # Si ya tienes una ventana, omite esta línea
                    ventana.title("Información del Usuario")

                    # Crear widgets para mostrar la información del usuario
                    label_usuario = tk.Label(ventana, text=f"Usuario: {usuario[0]}")
                    label_usuario.pack()


                    label_ultimo_acceso = tk.Label(ventana, text=f"Último acceso: {ultimo_acceso}")
                    label_ultimo_acceso.pack()

                    label_nombre = tk.Label(ventana, text=f"Nombre: {user.nombre}")
                    label_nombre.pack()
                   
                else:
                    messagebox.showerror("Error", "Usuario no encontrado en la base de datos")
            except ValueError:
                messagebox.showerror("Error", "Respuesta inválida del servidor")
        else:
            messagebox.showerror("Error", "No se pudo obtener la información del usuario")



    def crear_tarea(self):
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")
   

        # Etiqueta y campo de entrada para "Título"
        titulo_label = tk.Label(ventana, text="Título:")
        titulo_label.pack()

        titulo_entry = tk.Entry(ventana, width=60)
        titulo_entry.pack()

        # Etiqueta y campo de entrada para "Descripción"
        descripcion_label = tk.Label(ventana, text="Descripción:")
        descripcion_label.pack()

        descripcion_entry = tk.Entry(ventana, width=60)
        descripcion_entry.pack()

        # Etiqueta y campo de entrada para "Estado"
        estado_label = tk.Label(ventana, text="Estado:(Pendiente, En prodeso, Finalizada)")
        estado_label.pack()

        estado_entry = tk.Entry(ventana, width=60)
        estado_entry.pack()

        def crear_tareadb():
            administrador = administradorTarea('admintareas.db')
        
            id_value = administrador.generar_numero_aleatorio()
            titulo_value = titulo_entry.get()
            descripcion_value = descripcion_entry.get()
            estado_value = estado_entry.get()

            tarea = {
                    "id": id_value,
                    "titulo": titulo_value,
                    "descripcion": descripcion_value,
                    "estado": estado_value,
                    "actualizada": ""
                }
            print("Enviando datos de registro:", tarea)
            response = requests.post('http://127.0.0.1:8000/tarea', json=tarea)
            print("Respuesta del servidor:", response.status_code, response.json())

            if response.status_code == 200:
                    tarea_creada = response.json()
                    messagebox.showinfo("Tarea creada", f"Tarea creada:\nID: {tarea_creada['id']}\nTítulo: {tarea_creada['titulo']}\nDescripción: {tarea_creada['descripcion']}\nEstado: {tarea_creada['estado']}\nCreada: {tarea_creada['creada']} ")
            elif response.status_code == 422:
                    messagebox.showerror("Error", "El id debe ser un entero")
            elif response.status_code == 409:
                    messagebox.showerror("Error", "Ya hay una tarea con ese id")
            elif response.status_code == 400:
                    messagebox.showerror("Error", "Campos vacíos")
            else:
                    messagebox.showerror("Error", "Error al crear la tarea")

        btn_crear = tk.Button(ventana, text="Crear", command=crear_tareadb)
        btn_crear.pack(pady=10)
        
        

       
    def actualizar_estado(self):
   
        ventana = tk.Toplevel()
        ventana.title('Actualizar estado')
        ventana.geometry("300x300")

        def actualizar_estadodb(): 
            id = id_entry.get()
            estado = estado_entry.get()
            payload = {"id": id, "estado": estado}
            response = requests.put(f'http://127.0.0.1:8000/tarea/{id}/{estado}', json=payload)

            if response.status_code == 200:
                        messagebox.showinfo("Tarea actualizada", "Se ha actualizado la tarea")
            elif response.status_code == 404:
                        messagebox.showerror("Error", "No se encontro tarea con ese id")
            elif response.status_code == 422:
                         messagebox.showerror("Error", "El id no es un entero")
            else:
                    messagebox.showerror("Error", "No completo campo estado")

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()

        estado_label = tk.Label(ventana, text="Estado:")
        estado_label.pack()

        estado_entry = tk.Entry(ventana)
        estado_entry.pack()

        btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_estadodb)
        btn_actualizar.pack(pady=10)
        
    def eliminar_tarea(self):
        
        ventana = tk.Toplevel()
        ventana.title('Eliminar tarea')
        ventana.geometry("300x300")
        
        def eliminartarea_api(id):
            response = requests.delete(f'http://127.0.0.1:8000/tarea/{id}', json={"id": id})   
           
            
            if response.status_code == 200:
                messagebox.showinfo("Tarea eliminada", f"Tarea con {id} eliminada")
                ventana.destroy()
            elif response.status_code == 404: 
                messagebox.showerror("Error", "No se encontro tarea con ese id")
                
            elif response.status_code == 422:
                messagebox.showerror("Error", "El id debe ser un entero")
                
            else:
                messagebox.showerror("Error", "Complete id")
                
    
        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()
            
        btn_eliminar = tk.Button(ventana, text="Eliminar", command=lambda: eliminartarea_api(id_entry.get()))
        btn_eliminar.pack(pady=10)
    
    def traer_tarea(self):
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")

        def traertarea_api(id):
            response = requests.get(f'http://127.0.0.1:8000/tarea/{id}', json={"id": id})

            if response.status_code == 200:
                tarea_creada = response.json()
                messagebox.showinfo("Tarea", f"Tarea:\nID: {tarea_creada['id']}\nTítulo: {tarea_creada['titulo']}\nDescripción: {tarea_creada['descripcion']}\nEstado: {tarea_creada['estado']},\nCreada:{tarea_creada['creada']},\nActualizada: {tarea_creada['actualizada']}")
            elif response.status_code == 404:
                messagebox.showerror("Error", "No hay tarea con ese id")
            elif response.status_code == 422:
                messagebox.showerror("Error", "El id no es un entero")
            else:
                messagebox.showerror("Error", "Falta el id")
            
                  

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()
            
        btn_eliminar = tk.Button(ventana, text="Traer tarea", command=lambda: traertarea_api(id_entry.get()))
        btn_eliminar.pack(pady=10)
    
   


         
    

