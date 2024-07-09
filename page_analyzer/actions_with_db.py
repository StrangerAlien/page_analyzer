import psycopg2
from page_analyzer.secrets import DATABASE_URL
from datetime import datetime


def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except Exception as error:
        print('Can`t establish connection to database')
        raise error
    return conn


def save_url(url):
    with connect_db() as conn:
        with conn.cursor() as curs:
            curs.execute('''
                INSERT INTO urls (name, created_at) VALUES (%s, %s)
                RETURNING id;''',
                         (url, datetime.now()))
            url_data = curs.fetchone()
            conn.commit()
            return url_data


def save_url_check(tags_data):
    with connect_db() as conn:
        with conn.cursor() as curs:
            curs.execute('''
                INSERT INTO url_checks (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)''',
                         (
                             tags_data['id'],
                             tags_data['code'],
                             tags_data['h1'],
                             tags_data['title'],
                             tags_data['description'],
                             datetime.now()
                         )
                         )
            conn.commit()


def get_data_by_id(url_id):
    with connect_db() as conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM urls WHERE id=%s', (url_id,))
            existing = curs.fetchone()
            return existing


def get_data_by_name(url):
    with connect_db() as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM urls WHERE name=%s", (url,))
            existing = curs.fetchone()
            return existing


def get_data_all_urls():
    with connect_db() as conn:
        with conn.cursor() as curs:
            curs.execute('''
            SELECT
                urls.id,
                urls.name,
                url_checks.status_code,
                MAX(url_checks.created_at) AS last_check
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, urls.name, url_checks.status_code
            ORDER BY urls.id DESC;''',
                         )
            url_checks = curs.fetchall()
            return url_checks


def get_url_check(url_id):
    with connect_db() as conn:
        with conn.cursor() as curs:
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
                ORDER BY id DESC''', (url_id,)
                         )
            checks = curs.fetchall()
            return checks
