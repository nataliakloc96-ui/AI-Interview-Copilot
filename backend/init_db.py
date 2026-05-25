from db import get_conn


def init_db():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS users")

    cur.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


init_db()