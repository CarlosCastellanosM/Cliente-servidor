import requests
from requests.auth import HTTPBasicAuth

URL = 'http://localhost:5000/usuarios'
AUTH = HTTPBasicAuth('admin', '1234')

def obtener_usuarios():
    response = requests.get(URL, auth=AUTH)
    if response.status_code == 200:
        usuarios = response.json()
        print("Usuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios")

def agregar_usuario(nombre):
    nuevo_usuario = {"nombre": nombre}
    response = requests.post(URL, json=nuevo_usuario, auth=AUTH)
    if response.status_code == 201:
        print(f"Usuario agregado: {response.json()}")
    else:
        print("Error al agregar usuario")

def buscar_usuario_por_id(usuario_id):
    response = requests.get(f"{URL}/{usuario_id}", auth=AUTH)
    if response.status_code == 200:
        print(f"Usuario encontrado: {response.json()}")
    else:
        print("Usuario no encontrado")

def eliminar_usuario(usuario_id):
    response = requests.delete(f"{URL}/{usuario_id}", auth=AUTH)
    if response.status_code == 200:
        print(response.json()["mensaje"])
    else:
        print("Error al eliminar usuario")

if __name__ == '__main__':
    # Pruebas
    obtener_usuarios()
    agregar_usuario("Carlos")
    buscar_usuario_por_id(3)
    eliminar_usuario(3)