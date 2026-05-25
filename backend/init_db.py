from db import get_conn


def init_db():

    conn = get_conn()
    cur = conn.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS interview_history (
            id SERIAL PRIMARY KEY,
            email TEXT,
            score INT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


init_db()