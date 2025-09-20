from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Archivos de datos
USUARIOS_FILE = "data/usuarios.json"
TAREAS_FILE = "data/tareas.json"

# Asegurar que existan
if not os.path.exists("data"):
    os.makedirs("data")

for file in [USUARIOS_FILE, TAREAS_FILE]:
    if not os.path.isfile(file):
        with open(file, "w") as f:
            json.dump([], f)


@app.route("/")
def index():
    return render_template("index.html")


# Registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        telefono = request.form["telefono"]

        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)

        if any(u["correo"].lower() == correo.lower() for u in usuarios):
            return render_template(
                "register.html",
                error="Correo ya registrado.",
                nombre=nombre,
                apellidos=apellidos,
                correo=correo,
                telefono=telefono,
            )

        usuarios.append({
            "nombre": nombre,
            "apellidos": apellidos,
            "correo": correo,
            "contrasena": generate_password_hash(contrasena),
            "telefono": telefono,
        })

        with open(USUARIOS_FILE, "w") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

        return redirect(url_for("login"))

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)

        user = next((u for u in usuarios if u["correo"].lower() == correo.lower()), None)

        if user is None or not check_password_hash(user["contrasena"], contrasena):
            return render_template("login.html", error="Correo o contraseña incorrectos.", correo=correo)

        # Guardar sesión con nombre completo
        session["usuario"] = f"{user['nombre']} {user['apellidos']}"
        return redirect(url_for("worker"))

    return render_template("login.html")


# Cliente (tareas)
@app.route("/tareas", methods=["GET", "POST"])
def tareas():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        tarea = request.form["tarea"]
        descripcion = request.form["descripcion"]
        ofrezco = request.form["ofrezco"]
        ciudad = request.form["ciudad"]

        with open(TAREAS_FILE, "r") as f:
            tareas = json.load(f)

        tareas.append({
            "tarea": tarea,
            "descripcion": descripcion,
            "ofrezco": ofrezco,
            "ciudad": ciudad,
            "cliente": session.get("usuario"),
        })

        with open(TAREAS_FILE, "w") as f:
            json.dump(tareas, f, indent=4, ensure_ascii=False)

        return redirect(url_for("tareas"))

    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    return render_template("customer.html", tareas=tareas, usuario=session.get("usuario"))


# Trabajador
@app.route("/worker")
def worker():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("worker.html", usuario=session.get("usuario"))


# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
