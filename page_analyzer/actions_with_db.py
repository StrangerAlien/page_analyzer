from psycopg2.pool import SimpleConnectionPool
from page_analyzer.secrets import DATABASE_URL
from datetime import datetime

postgresql_pool = SimpleConnectionPool(1, 20, dsn=DATABASE_URL)


def save_url(url):
    conn = postgresql_pool.getconn()
    curs = conn.cursor()
    curs.execute('''
        INSERT INTO urls (
            name,
            created_at)
        VALUES (%s, %s)
        RETURNING id;''', (url, datetime.now()))
    url_data = curs.fetchone()
    conn.commit()
    curs.close()
    postgresql_pool.putconn(conn)
    return url_data


def save_url_check(tags_data):
    conn = postgresql_pool.getconn()
    curs = conn.cursor()
    curs.execute('''
        INSERT INTO url_checks (
            url_id,
            status_code,
            h1,
            title,
            description,
            created_at )
        VALUES (%s, %s, %s, %s, %s, %s)''', (
        tags_data['id'],
        tags_data['code'],
        tags_data['h1'],
        tags_data['title'],
        tags_data['description'],
        datetime.now()))
    conn.commit()
    curs.close()
    postgresql_pool.putconn(conn)


def get_data_by_id(url_id):
    conn = postgresql_pool.getconn()
    curs = conn.cursor()
    curs.execute('''
        SELECT * FROM urls WHERE id=%s''', (url_id,))
    existing = curs.fetchone()
    curs.close()
    postgresql_pool.putconn(conn)
    return existing


def get_data_by_name(url):
    conn = postgresql_pool.getconn()
    curs = conn.cursor()
    curs.execute('''
        SELECT * FROM urls WHERE name=%s''', (url,))
    existing = curs.fetchone()
    curs.close()
    postgresql_pool.putconn(conn)
    return existing


def get_data_all_urls():
    conn = postgresql_pool.getconn()
    curs = conn.cursor()
    curs.execute('''
        SELECT
            urls.id,
            urls.name,
            url_checks.status_code,
            MAX(url_checks.created_at) AS last_check
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, urls.name, url_checks.status_code
        ORDER BY urls.id DESC;''', )
    url_checks = curs.fetchall()
    curs.close()
    postgresql_pool.putconn(conn)
    return url_checks


def get_url_check(url_id):
    conn = postgresql_pool.getconn()
    curs = conn.cursor()
    curs.execute('''
        SELECT
            id,
            status_code,
            h1,
            title,
            description,
            created_at
        FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC''', (url_id,))
    checks = curs.fetchall()
    curs.close()
    postgresql_pool.putconn(conn)
    return checks
