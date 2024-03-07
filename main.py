from multiprocessing import Process
from interfaz.interfaz import VentanaPrincipal
from uvicorn import Config, Server
from arApi.api import app
import sys
print(sys.path)


def iniciar_ventana():
    ventana = VentanaPrincipal()
    ventana.mainloop()

def iniciar_servidor():
    config = Config(app="main:app", host="0.0.0.0", port=8000, reload=True)
    server = Server(config)
    server.run()

if __name__ == "__main__":
    ventana_thread = Process(target=iniciar_ventana)
    servidor_thread = Process(target=iniciar_servidor)

    servidor_thread.start()
    ventana_thread.start()
 
  