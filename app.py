from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

DATA_FILE = "data/usuarios.json"

# Asegurar que exista el archivo
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        # Cargar usuarios existentes
        with open(DATA_FILE, "r") as f:
            usuarios = json.load(f)

        # Agregar nuevo usuario
        usuarios.append({
            "nombre": nombre,
            "email": email,
            "password": password  # (⚠ en producción deberías cifrar la contraseña)
        })

        # Guardar en JSON
        with open(DATA_FILE, "w") as f:
            json.dump(usuarios, f, indent=4)

        return redirect(url_for("index"))  # redirigir al inicio después de registrarse

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
