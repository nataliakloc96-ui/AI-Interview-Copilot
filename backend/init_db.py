from db import get_conn

def init_db():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE,
                password_hash TEXT
                )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()