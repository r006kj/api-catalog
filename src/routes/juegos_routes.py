from flask import Blueprint, request, jsonify
from src.db import get_connection

juegos_bp = Blueprint("juegos", __name__)


@juegos_bp.route("/juegos", methods=["GET"])
def listar_juegos():
    """Listar todos los juegos
    ---
    tags: [juegos]
    responses:
      200:
        description: Lista de juegos
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM juegos")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200


@juegos_bp.route("/juegos/<int:id>", methods=["GET"])
def obtener_juego(id):
    """Obtener un juego por id
    ---
    tags: [juegos]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Juego encontrado
      404:
        description: Juego no encontrado
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM juegos WHERE id = %s", (id,))
    juego = cursor.fetchone()
    cursor.close()
    conn.close()
    if juego is None:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify(juego), 200


@juegos_bp.route("/juegos", methods=["POST"])
def crear_juego():
    """Crear un juego
    ---
    tags: [juegos]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo: {type: string}
            genero: {type: string}
            complejidad: {type: string}
            jugadores_min: {type: integer}
            jugadores_max: {type: integer}
            editorial_id: {type: integer}
    responses:
      201:
        description: Juego creado
      400:
        description: Falta el campo titulo
    """
    body = request.get_json(silent=True) or {}
    if not body.get("titulo"):
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO juegos
           (titulo, genero, complejidad, jugadores_min, jugadores_max, editorial_id)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            body.get("titulo"),
            body.get("genero"),
            body.get("complejidad"),
            body.get("jugadores_min"),
            body.get("jugadores_max"),
            body.get("editorial_id"),
        ),
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": nuevo_id, **body}), 201


@juegos_bp.route("/juegos/<int:id>", methods=["PUT"])
def actualizar_juego(id):
    """Actualizar un juego
    ---
    tags: [juegos]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo: {type: string}
            genero: {type: string}
            complejidad: {type: string}
            jugadores_min: {type: integer}
            jugadores_max: {type: integer}
            editorial_id: {type: integer}
    responses:
      200:
        description: Juego actualizado
      404:
        description: Juego no encontrado
    """
    body = request.get_json(silent=True) or {}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE juegos SET
           titulo = %s, genero = %s, complejidad = %s,
           jugadores_min = %s, jugadores_max = %s, editorial_id = %s
           WHERE id = %s""",
        (
            body.get("titulo"),
            body.get("genero"),
            body.get("complejidad"),
            body.get("jugadores_min"),
            body.get("jugadores_max"),
            body.get("editorial_id"),
            id,
        ),
    )
    conn.commit()
    afectadas = cursor.rowcount
    cursor.close()
    conn.close()
    if afectadas == 0:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify({"id": id, **body}), 200


@juegos_bp.route("/juegos/<int:id>", methods=["DELETE"])
def eliminar_juego(id):
    """Eliminar un juego
    ---
    tags: [juegos]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Juego eliminado
      404:
        description: Juego no encontrado
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
    conn.commit()
    afectadas = cursor.rowcount
    cursor.close()
    conn.close()
    if afectadas == 0:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify({"mensaje": f"Juego con id: {id} eliminado"}), 200
