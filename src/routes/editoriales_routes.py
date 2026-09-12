from flask import Blueprint, jsonify
from src.db import get_connection

editoriales_bp = Blueprint("editoriales", __name__)


@editoriales_bp.route("/editoriales", methods=["GET"])
def listar_editoriales():
    """Listar todas las editoriales
    ---
    tags: [editoriales]
    responses:
      200:
        description: Lista de editoriales
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM editoriales")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200


@editoriales_bp.route("/editoriales/<int:id>", methods=["GET"])
def obtener_editorial(id):
    """Obtener una editorial por id
    ---
    tags: [editoriales]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Editorial encontrada
      404:
        description: Editorial no encontrada
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM editoriales WHERE id = %s", (id,))
    editorial = cursor.fetchone()
    cursor.close()
    conn.close()
    if editorial is None:
        return jsonify({"error": "Editorial no encontrada"}), 404
    return jsonify(editorial), 200
