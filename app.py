import os
from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# PostgreSQL connection using environment variables
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD")
)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    message TEXT
)
""")
conn.commit()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    cur.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['message'])
    )
    conn.commit()
    return jsonify({"message": "Message saved successfully!"})

# Admin panel route
@app.route('/admin')
def admin():
    password = request.args.get('key')
    if password != os.environ.get("ADMIN_KEY", "admin123"):
        return "Unauthorized"
    cur.execute("SELECT * FROM contacts ORDER BY id DESC")
    data = cur.fetchall()
    return render_template("admin.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
