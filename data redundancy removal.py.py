from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = 'redundancy.db'

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE IF NOT EXISTS entries(id INTEGER PRIMARY KEY, data TEXT UNIQUE)')
    conn.commit()
    conn.close()

@app.route('/add', methods=['POST'])
def add():
    new = request.json.get('data')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO entries(data) VALUES(?)', (new,))
        conn.commit()
        return jsonify({'status':'added'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'status':'duplicate'}), 409
    finally:
        conn.close()

@app.route('/list')
def list_all():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT data FROM entries')
    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)