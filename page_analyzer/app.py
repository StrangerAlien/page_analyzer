import requests

from flask import (Flask, render_template, request, flash,
                   redirect, url_for, get_flashed_messages)

from page_analyzer.correct_url import correct_url
from page_analyzer.parse_html import parse_html
from page_analyzer.secrets import SECRET_KEY
from page_analyzer import actions_with_db as db

from urllib.parse import urlparse, urlunparse

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
                           url_id=url_id, url_data=url_data, name=name,
                           messages=messages, checks=checks, date=date), 200


@app.post('/urls')
def post_url():
    data = request.form.to_dict()
    url = data.get('url').lower()
    errors = correct_url(url)

    if errors:
        for error in errors:
            flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

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
