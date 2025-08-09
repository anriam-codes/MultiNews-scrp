from db_config import get_db_conn

def insert_articles(articles):
    conn = get_db_conn()
    print("Connevcted to Postgres")
    cur = conn.cursor()
    for a in articles:
        cur.execute("""
            INSERT INTO news (source, title, url)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (a["source"], a["title"], a["url"]))
    conn.commit()
    cur.close()
    conn.close()
