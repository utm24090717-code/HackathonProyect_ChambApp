from flask import Flask, render_template, request, redirect, url_for, session 
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesario para manejar sesiones

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


# Registro de usuarios
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

        # Validar correo único
        if any(u["correo"].lower() == correo.lower() for u in usuarios):
            return render_template(
                "register.html",
                error="Correo ya registrado.",
                nombre=nombre,
                apellidos=apellidos,
                correo=correo,
                telefono=telefono,
            )

        # Guardar con contraseña encriptada
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


# Login de usuarios (validación correo + contraseña)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)

        # Buscar usuario por correo
        user = next((u for u in usuarios if u["correo"].lower() == correo.lower()), None)

        if user is None:
            return render_template("login.html", error="Correo o contraseña incorrectos.", correo=correo)

        # Validar contraseña
        if not check_password_hash(user["contrasena"], contrasena):
            return render_template("login.html", error="Correo o contraseña incorrectos.", correo=correo)

        # Si todo bien → guardar sesión
        session["usuario"] = f"{user['nombre']} {user['apellidos']}"
        session["correo"] = user["correo"]   # Guardamos también el correo para filtrar tareas
        return redirect(url_for("tareas"))

    return render_template("login.html")


# Crear y listar tareas (CLIENTE)
@app.route("/tareas", methods=["GET", "POST"])
def tareas():
    if "usuario" not in session or "correo" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        titulo = request.form["tarea"]
        descripcion = request.form["descripcion"]
        ofrezco = request.form["ofrezco"]
        ciudad = request.form["ciudad"]

        with open(TAREAS_FILE, "r") as f:
            tareas = json.load(f)

        # Guardamos la tarea con el correo del creador
        tareas.append({
            "titulo": titulo,
            "descripcion": descripcion,
            "ofrezco": ofrezco,
            "ciudad": ciudad,
            "creador": session["correo"]  
        })

        with open(TAREAS_FILE, "w") as f:
            json.dump(tareas, f, indent=4, ensure_ascii=False)

        return redirect(url_for("tareas"))

    # Listar tareas (todas, solo para que el cliente vea lo que subió)
    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    return render_template("customer.html", tareas=tareas, usuario=session.get("usuario"))


# Vista TRABAJADOR (solo ve tareas de otros usuarios)
@app.route("/worker")
def worker():
    if "usuario" not in session or "correo" not in session:
        return redirect(url_for("login"))

    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    # Filtrar → excluir las creadas por el usuario logueado
    tareas_disponibles = [t for t in tareas if t["creador"] != session["correo"]]

    return render_template("worker.html", usuario=session.get("usuario"), tareas=tareas_disponibles)


# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("correo", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
