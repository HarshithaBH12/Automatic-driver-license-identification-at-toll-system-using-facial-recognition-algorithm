from flask import Flask, render_template, jsonify
import sqlite3
import requests
from datetime import datetime

app = Flask(_name_)

DB_FILE = "data_store.db"
API_URL = "https://aislyntech.com/Api/e-get.php"

# Ensure table exists with correct columns
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT,
            vehicle_number TEXT,
            license_number TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Fetch current data from API
def fetch_current_data():
    try:
        response = requests.get(API_URL)
        data = response.json().get("data", [])
        return data
    except Exception as e:
        print("Error fetching API data:", e)
        return []

# Check if an item already exists in history
def exists_in_history(item):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT 1 FROM history
        WHERE name=? AND status=? AND vehicle_number=? AND license_number=?
    ''', (
        item.get("name"),
        item.get("status"),
        item.get("vehicle_number"),
        item.get("license_number")
    ))
    exists = c.fetchone() is not None
    conn.close()
    return exists

# Store data in history if not exists
def store_history(item):
    if not exists_in_history(item):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO history (name, status, vehicle_number, license_number, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            item.get("name"),
            item.get("status"),
            item.get("vehicle_number"),
            item.get("license_number"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

@app.route("/")
def index():
    current_data = fetch_current_data()
    for item in current_data:
        store_history(item)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY created_at DESC")
    history = c.fetchall()
    conn.close()

    return render_template("index.html", current_data=current_data, history=history)

# API route to get history details
@app.route("/history/<int:id>")
def get_history(id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE id = ?", (id,))
    row = c.fetchone()
    conn.close()
    if row:
        data = {
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "vehicle_number": row[3],
            "license_number": row[4],
            "created_at": row[5]
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Not found"}), 404

if _name_ == "_main_":
    init_db()
    app.run(debug=True)