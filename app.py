from flask import Flask, render_template, request, redirect, url_for, flash, session
import json, os

app = Flask(__name__)

DATA_FILE = "data/usuarios.json"

# Asegurar que exista la carpeta y el archivo
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
        apellidos = request.form["apellidos"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]

        # Cargar usuarios existentes
        try:
            with open(DATA_FILE, "r") as f:
                usuarios = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            usuarios = []

        # 🔹 Validar correo o teléfono duplicado
        for u in usuarios:
            if u["correo"].lower() == correo.lower():
                return render_template(
                    "register.html",
                    error="⚠️ Este correo ya está registrado.",
                    nombre=nombre,
                    apellidos=apellidos,
                    correo=correo,
                    telefono=telefono
                )
            if u["telefono"] == telefono:
                return render_template(
                    "register.html",
                    error="⚠️ Este número telefónico ya está registrado.",
                    nombre=nombre,
                    apellidos=apellidos,
                    correo=correo,
                    telefono=telefono
                )

        # Agregar nuevo usuario
        usuarios.append({
            "nombre": nombre,
            "apellidos": apellidos,
            "correo": correo,
            "telefono": telefono
        })

        # Guardar en JSON
        with open(DATA_FILE, "w") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

        return redirect(url_for("index"))

    return render_template("register.html")

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = request.form['password']

    # Aquí deberías validar contra tu base de datos
    # Ejemplo con credenciales fijas:
    if correo == "admin@chambapp.com" and password == "12345":
        session['usuario'] = correo
        flash("Has iniciado sesión correctamente", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Correo o contraseña incorrectos", "error")
        return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)
