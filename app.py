from flask import Flask,request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="192.168.109.133",
        user="myuser",
        password="mypass",
        database="DBdev",
        port=3306
    )
    return conn

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/users")
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


@app.route("/update-age")
def update_age_url():
    user_id = request.args.get("uid")
    new_age = request.args.get("age")

    if not user_id or not new_age:
        return "Missing id or age", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET age = %s WHERE uid = %s", (new_age, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return f"Updated user {user_id} age to {new_age}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)