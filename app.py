from flask import Flask, render_template, request, redirect, url_for, session 
from werkzeug.security import generate_password_hash, check_password_hash
import json, os, requests

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


# Login de usuarios
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)

        # Buscar usuario
        user = next((u for u in usuarios if u["correo"].lower() == correo.lower()), None)

        if user is None:
            return render_template("login.html", error="Correo o contraseña incorrectos.", correo=correo)

        if not check_password_hash(user["contrasena"], contrasena):
            return render_template("login.html", error="Correo o contraseña incorrectos.", correo=correo)

        # Guardar sesión
        session["usuario"] = f"{user['nombre']} {user['apellidos']}"
        session["correo"] = user["correo"]
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

        tarea_id = len(tareas)

        tareas.append({
            "id": tarea_id,
            "titulo": titulo,
            "descripcion": descripcion,
            "ofrezco": ofrezco,
            "ciudad": ciudad,
            "creador": session["correo"],
            "trabajador": None,
            "pagada": False
        })

        with open(TAREAS_FILE, "w") as f:
            json.dump(tareas, f, indent=4, ensure_ascii=False)

        return redirect(url_for("tareas"))

    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    return render_template("customer.html", tareas=tareas, usuario=session.get("usuario"))


# Vista TRABAJADOR
@app.route("/worker")
def worker():
    if "usuario" not in session or "correo" not in session:
        return redirect(url_for("login"))

    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    tareas_disponibles = [t for t in tareas if t["creador"] != session["correo"]]

    return render_template("worker.html", usuario=session.get("usuario"), tareas=tareas_disponibles)


# Aceptar tarea
@app.route("/aceptar/<int:tarea_id>", methods=["POST"])
def aceptar_tarea(tarea_id):
    if "usuario" not in session or "correo" not in session:
        return redirect(url_for("login"))

    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    for t in tareas:
        if t.get("id") == tarea_id and not t.get("trabajador"):
            t["trabajador"] = session["usuario"]
            break

    with open(TAREAS_FILE, "w") as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)

    return redirect(url_for("worker"))


# Pagar tarea (Cliente → Trabajador)
@app.route("/pagar/<int:tarea_id>", methods=["POST"])
def pagar_tarea(tarea_id):
    if "usuario" not in session or "correo" not in session:
        return redirect(url_for("login"))

    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    tarea = next((t for t in tareas if t.get("id") == tarea_id), None)
    if not tarea:
        return "Tarea no encontrada", 404

    if not tarea.get("trabajador"):
        return "No se puede pagar sin trabajador", 400

    # 🚀 Simulación de pago con Open Payments
    try:
        payload = {
            "amount": tarea["ofrezco"],
            "assetCode": "USD",
            "assetScale": 2,
            "receiver": "https://openpayments.guide/api/payments/receiver",
        }

        r = requests.post("https://openpayments.guide/api/payments", json=payload)

        if r.status_code == 201:
            tarea["pagada"] = True
        else:
            print("Error de pago:", r.text)

    except Exception as e:
        print("Error conectando a Open Payments:", e)

    with open(TAREAS_FILE, "w") as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)

    return redirect(url_for("tareas"))


if __name__ == "__main__":
    app.run(debug=True)
