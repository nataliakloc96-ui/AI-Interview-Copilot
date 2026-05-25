from db import get_conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        ALTER TABLE users
        RENAME COLUMN password TO password_hash
    """)

    conn.commit()

    cur.close()
    conn.close()


init_db()