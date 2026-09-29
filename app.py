
from flask import Flask, render_template, jsonify, request, redirect
from db import get_connection

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, price, description
        FROM coffee
    """)

    coffees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', coffees=coffees)


@app.route('/coffee', methods=['GET'])
def get_coffee():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, price, description
        FROM coffee
    """)

    rows = cursor.fetchall()

    coffees = []

    for row in rows:
        coffees.append({
            "id": row.id,
            "name": row.name,
            "price": float(row.price),
            "description": row.description
        })

    cursor.close()
    conn.close()

    return jsonify(coffees)


@app.route('/coffee', methods=['POST'])
def add_coffee():
    if request.is_json:
        data = request.get_json()

        name = data['name']
        price = data['price']
        description = data['description']
    else:
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO coffee (name, price, description)
        VALUES (?, ?, ?)
    """, (name, price, description))

    conn.commit()

    cursor.close()
    conn.close()

    if request.is_json:
        return jsonify({
            "message": "Coffee added successfully"
        }), 201

    return redirect('/home')


@app.route('/coffee/<int:id>', methods=['PUT'])
def update_coffee(id):
    data = request.get_json()

    name = data['name']
    price = data['price']
    description = data['description']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE coffee
        SET name = ?, price = ?, description = ?
        WHERE id = ?
    """, (name, price, description, id))

    conn.commit()

    rows_updated = cursor.rowcount

    cursor.close()
    conn.close()

    if rows_updated == 0:
        return jsonify({
            "message": "Coffee not found"
        }), 404

    return jsonify({
        "message": "Coffee updated successfully"
    })


@app.route('/coffee/<int:id>', methods=['DELETE'])
def delete_coffee(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM coffee
        WHERE id = ?
    """, (id,))

    conn.commit()

    rows_deleted = cursor.rowcount

    cursor.close()
    conn.close()

    if rows_deleted == 0:
        return jsonify({
            "message": "Coffee not found"
        }), 404

    return jsonify({
        "message": "Coffee deleted successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)

