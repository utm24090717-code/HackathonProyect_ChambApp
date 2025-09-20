from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Archivo donde se guardarán los registros
USUARIOS_FILE = "usuarios.json"

# Función para guardar los datos en JSON
def guardar_usuario(usuario):
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []

    usuarios.append(usuario)

    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


@app.route("/")
def registro():
    return render_template("registro.html")


@app.route("/registro", methods=["POST"])
def registrar():
    usuario = {
        "nombre": request.form["nombre"],
        "apellidos": request.form["apellidos"],
        "correo": request.form["correo"],
        "numero": request.form["numero"],
        "contrasena": request.form["contrasena"]
    }

    guardar_usuario(usuario)

    # Redirigir a la página de iniciar sesión
    return redirect(url_for("iniciar_sesion"))


@app.route("/iniciar_sesion")
def iniciar_sesion():
    return render_template("iniciar_sesion.html")


if __name__ == "__main__":
    app.run(debug=True)
