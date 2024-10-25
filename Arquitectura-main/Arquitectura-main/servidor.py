from flask import Flask, jsonify, request, abort
from functools import wraps

app = Flask(__name__)

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "María"}
    ]
}

# Autenticación básica
def requiere_autenticacion(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'admin' or auth.password != '1234':
            return abort(401)  # No autorizado
        return f(*args, **kwargs)
    return decorador

# Ruta para obtener todos los usuarios (GET)
@app.route('/usuarios', methods=['GET'])
@requiere_autenticacion
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])

# Ruta para obtener un usuario por ID (GET)
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
@requiere_autenticacion
def obtener_usuario_por_id(usuario_id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == usuario_id), None)
    if usuario:
        return jsonify(usuario)
    else:
        return abort(404, description="Usuario no encontrado")

# Ruta para agregar un usuario (POST)
@app.route('/usuarios', methods=['POST'])
@requiere_autenticacion
def agregar_usuario():
    nuevo_usuario = request.get_json()
    if not nuevo_usuario or "nombre" not in nuevo_usuario:
        return abort(400, description="Datos inválidos")

    nuevo_usuario["id"] = len(base_datos["usuarios"]) + 1  # Generar ID automático
    base_datos["usuarios"].append(nuevo_usuario)
    return jsonify(nuevo_usuario), 201

# Ruta para eliminar un usuario por ID (DELETE)
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_usuario(usuario_id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == usuario_id), None)
    if usuario:
        base_datos["usuarios"].remove(usuario)
        return jsonify({"mensaje": f"Usuario con ID {usuario_id} eliminado"}), 200
    else:
        return abort(404, description="Usuario no encontrado")

if __name__ == '__main__':
    app.run(port=5000)