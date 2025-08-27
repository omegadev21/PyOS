import os
import bcrypt
import sqlite3
from typing import Optional, Dict

DB_PATH = "system_files/users.db"

def _conn():
    os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash BLOB NOT NULL,
        salt BLOB NOT NULL,
        sudo INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_user(username: str, password: str, sudo: bool=False):
    init_db()
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,password_hash,salt,sudo) VALUES (?, ?, ?, ?)",
                (username, pw_hash, salt, 1 if sudo else 0))
    conn.commit()
    conn.close()

def remove_user(username: str):
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_user(username: str) -> Optional[Dict]:
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash, salt, sudo FROM users WHERE username = ?", (username,))
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    return {"username": r["username"], "password_hash": r["password_hash"], "salt": r["salt"], "sudo": bool(r["sudo"])}

def verify_user(username: str, password: str) -> bool:
    u = get_user(username)
    if not u:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), u["password_hash"])
    except Exception:
        return False

def set_password(username: str, password: str):
    init_db()
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    conn = _conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash = ?, salt = ? WHERE username = ?", (pw_hash, salt, username))
    conn.commit()
    conn.close()

def set_sudo(username: str, sudo: bool):
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET sudo = ? WHERE username = ?", (1 if sudo else 0, username))
    conn.commit()
    conn.close()

def list_users():
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT username, sudo FROM users")
    rows = cur.fetchall()
    conn.close()
    return [{"username": r["username"], "sudo": bool(r["sudo"])} for r in rows]

def make_db():
    init_db()
    add_user('root', 'toor', True)