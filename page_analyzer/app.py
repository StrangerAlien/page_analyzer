import requests
from flask import (Flask, render_template, request, flash,
                   redirect, url_for, get_flashed_messages)

from page_analyzer.secrets import SECRET_KEY
from page_analyzer import actions_with_db as db

from urllib.parse import urlparse, urlunparse
import validators

from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html', messages=()), 200


@app.get('/urls')
def get_all_urls():
    url_data = db.get_data_all_urls()
    return render_template('urls.html', urls=url_data)


@app.get('/urls/<int:url_id>')
def get_url(url_id):
    url_data = db.get_data_by_id(url_id)
    name, date = url_data[1], url_data[2]
    checks = db.get_url_check(url_id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html',
                           url_id=url_id, name=name, date=date,
                           messages=messages, checks=checks)


@app.post('/urls')
def post_url():
    data = request.form.to_dict()
    url = data.get('url').lower()
    errors = correct_url(url)

    if errors:
        for error in errors:
            flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url='', messages=messages), 422

    parsed_url = urlparse(url)
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    exist_url = db.get_data_by_name(new_url)

    if exist_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', url_id=exist_url[0]), 302)

    new_id = db.save_url(new_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', url_id=new_id[0]), 302)


@app.post('/urls/<int:url_id>/checks')
def post_url_checks(url_id):
    url = db.get_data_by_id(url_id)

    try:
        response = requests.get(url[1], timeout=15)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', url_id=url_id), 302)

    status_code = response.status_code

    tags_data = parse_html(response.text)
    tags_data['id'] = url_id
    tags_data['code'] = status_code

    db.save_url_check(tags_data)

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', url_id=url_id), 302)


###################################


def correct_url(url):
    errors = []
    parsed_url = urlparse(url)

    if all([parsed_url.scheme, parsed_url.netloc]) and len(url) > 255:
        errors.append('URL превышает 255 символов')
    if validators.url(url) is not True:
        errors.append('Некорректный URL')
    return errors


def parse_html(page_content):
    result = {}
    soup = BeautifulSoup(page_content, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    result['h1'] = h1.get_text().strip() if h1 else ''
    result['title'] = title.get_text().strip() if title else ''
    result['description'] = (
        description.get('content', '').strip()) if description else ''
    return result
