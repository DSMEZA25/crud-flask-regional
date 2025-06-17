from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    conn = sqlite3.connect("db.sqlite")
    return conn

@app.route("/")
def formulario():
    return render_template("form.html")

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    motivo = request.form["motivo"]
    regional = request.form["regional"]

    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO personas (nombre, motivo, regional) VALUES (?, ?, ?)", (nombre, motivo, regional))
    conn.commit()
    conn.close()
    return redirect(url_for("formulario"))

@app.route("/personas")
def personas():
    filtro = request.args.get("regional", "")
    conn = conectar()
    cur = conn.cursor()
    if filtro:
        cur.execute("SELECT * FROM personas WHERE regional = ?", (filtro,))
    else:
        cur.execute("SELECT * FROM personas")
    personas = cur.fetchall()
    conn.close()
    return render_template("list.html", personas=personas, filtro=filtro)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = conectar()
    cur = conn.cursor()
    if request.method == "POST":
        nombre = request.form["nombre"]
        motivo = request.form["motivo"]
        regional = request.form["regional"]
        cur.execute("UPDATE personas SET nombre=?, motivo=?, regional=? WHERE id=?", (nombre, motivo, regional, id))
        conn.commit()
        conn.close()
        return redirect(url_for("personas"))
    else:
        cur.execute("SELECT * FROM personas WHERE id=?", (id,))
        persona = cur.fetchone()
        conn.close()
        return render_template("edit.html", persona=persona)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM personas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("personas"))

if __name__ == "__main__":
    conn = conectar()
    conn.execute("""CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        motivo TEXT NOT NULL,
        regional TEXT NOT NULL
    )""")
    conn.close()
    app.run(debug=True)
