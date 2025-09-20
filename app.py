from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

# Archivos de datos
USUARIOS_FILE = "data/usuarios.json"
TAREAS_FILE = "data/tareas.json"

# Asegurar que existan
for file in [USUARIOS_FILE, TAREAS_FILE]:
    if not os.path.exists("data"):
        os.makedirs("data")
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
        correo = request.form["correo"]

        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)

        # Validar correo único
        if any(u["correo"].lower() == correo.lower() for u in usuarios):
            return render_template("register.html", error="Correo ya registrado.", nombre=nombre, correo=correo)

        usuarios.append({"nombre": nombre, "correo": correo})

        with open(USUARIOS_FILE, "w") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

        return redirect(url_for("index"))

    return render_template("register.html")

# Crear tareas
@app.route("/tareas", methods=["GET", "POST"])
def tareas():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]

        with open(TAREAS_FILE, "r") as f:
            tareas = json.load(f)

        tareas.append({"titulo": titulo, "descripcion": descripcion})

        with open(TAREAS_FILE, "w") as f:
            json.dump(tareas, f, indent=4, ensure_ascii=False)

        return redirect(url_for("tareas"))

    # Listar tareas
    with open(TAREAS_FILE, "r") as f:
        tareas = json.load(f)

    return render_template("tareas.html", tareas=tareas)


if __name__ == "__main__":
    app.run(debug=True)
