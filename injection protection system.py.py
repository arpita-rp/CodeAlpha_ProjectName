from flask import Flask, request, jsonify
import sqlite3
from Crypto.Cipher import AES
import base64

app = Flask(__name__)
DB = 'secure.db'
KEY = b'ThisIsA256BitKeyForAES_12345678'

def encrypt(raw):
    raw = raw + ' ' * ((16 - len(raw) % 16) % 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw.encode())).decode()

def decrypt(enc):
    cipher = AES.new(KEY, AES.MODE_ECB)
    dec = cipher.decrypt(base64.b64decode(enc))
    return dec.decode().rstrip()

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json['username']
    pwd = request.json['password']
    pwd_enc = encrypt(pwd)
    conn = sqlite3.connect(DB)
    try:
        conn.execute('INSERT INTO users(username,password) VALUES(?,?)', (username, pwd_enc))
        conn.commit()
        return jsonify({'status':'registered'})
    except sqlite3.IntegrityError:
        return jsonify({'status':'user exists'}), 409
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    pwd = request.json['password']
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row and decrypt(row[0]) == pwd:
        return jsonify({'status':'login successful'})
    return jsonify({'status':'invalid credentials'}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)