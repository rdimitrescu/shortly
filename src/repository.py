import psycopg

def db_single_write(long_url:str, url_hash:str):
    with psycopg.connect("dbname=shortly_db user=dev ") as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO link_entries (long_url, url_hash) VALUES (%s, %s)",(long_url, url_hash))