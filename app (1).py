import os
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
        )
    except mysql.connector.Error as e:
        print(e)
    return conn


# ---------- JUEGOS ----------

@app.route("/juegos", methods=["GET", "POST"])
def juegos():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "GET":
        cursor.execute("SELECT * FROM juegos")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data), 200

    if request.method == "POST":
        body = request.get_json()
        sql = """INSERT INTO juegos
                 (titulo, genero, complejidad, jugadores_min, jugadores_max, editorial_id)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            body.get("titulo"),
            body.get("genero"),
            body.get("complejidad"),
            body.get("jugadores_min"),
            body.get("jugadores_max"),
            body.get("editorial_id"),
        ))
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": nuevo_id, **body}), 201


@app.route("/juegos/<int:id>", methods=["GET", "PUT", "DELETE"])
def juego(id):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "GET":
        cursor.execute("SELECT * FROM juegos WHERE id = %s", (id,))
        juego = cursor.fetchone()
        cursor.close()
        conn.close()
        if juego is None:
            return jsonify({"error": "Juego no encontrado"}), 404
        return jsonify(juego), 200

    if request.method == "PUT":
        body = request.get_json()
        sql = """UPDATE juegos SET
                 titulo = %s, genero = %s, complejidad = %s,
                 jugadores_min = %s, jugadores_max = %s, editorial_id = %s
                 WHERE id = %s"""
        cursor.execute(sql, (
            body.get("titulo"),
            body.get("genero"),
            body.get("complejidad"),
            body.get("jugadores_min"),
            body.get("jugadores_max"),
            body.get("editorial_id"),
            id,
        ))
        conn.commit()
        afectadas = cursor.rowcount
        cursor.close()
        conn.close()
        if afectadas == 0:
            return jsonify({"error": "Juego no encontrado"}), 404
        return jsonify({"id": id, **body}), 200

    if request.method == "DELETE":
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
        conn.commit()
        afectadas = cursor.rowcount
        cursor.close()
        conn.close()
        if afectadas == 0:
            return jsonify({"error": "Juego no encontrado"}), 404
        return jsonify({"mensaje": f"Juego con id: {id} eliminado"}), 200


# ---------- EDITORIALES ----------

@app.route("/editoriales", methods=["GET"])
def editoriales():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM editoriales")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200


@app.route("/editoriales/<int:id>", methods=["GET"])
def editorial(id):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM editoriales WHERE id = %s", (id,))
    editorial = cursor.fetchone()
    cursor.close()
    conn.close()
    if editorial is None:
        return jsonify({"error": "Editorial no encontrada"}), 404
    return jsonify(editorial), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
