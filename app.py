from flask import Flask, render_template, request, redirect, url_for
import pymysql
from config import DB_CONFIG

app = Flask(__name__)

# -----------------------------
# Conexión a la base de datos
# -----------------------------
def get_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# -----------------------------
# Rutas
# -----------------------------
@app.route("/")
def home():
    return render_template("inicio_sesion.html")

@app.route("/iniciar_sesion")
def home():
    return render_template("iniciar_sesion.html")


@app.route("/usuarios")
def usuarios():
    conexion = get_connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, correo FROM usuarios")
        data = cursor.fetchall()
    conexion.close()
    return render_template("usuarios.html", usuarios=data)

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")

        conexion = get_connection()
        with conexion.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, correo))
            conexion.commit()
        conexion.close()

        return redirect(url_for("usuarios"))

    return render_template("formulario.html")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
