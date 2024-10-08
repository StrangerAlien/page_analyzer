### Hexlet tests and linter status:
[![Actions Status](https://github.com/StrangerAlien/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/StrangerAlien/python-project-83/actions)
[![linter](https://github.com/StrangerAlien/python-project-83/actions/workflows/linter.yml/badge.svg)](https://github.com/StrangerAlien/python-project-83/actions/workflows/linter.yml)

### Описание
Page Analyzer – это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с PageSpeed Insights:

![Demo](page_analyzer/static/page_analyzer.gif)


### Проверить работу и протестировать можно по ссылке:

[![svg](page_analyzer/static/page_analyzer.svg)](https://python-project-83-61qx.onrender.com)


### Dependencies

- python = "^3.10"
- requests = "^2.32.3"
- flask = "^3.0.3"
- validators = "^0.30.0"
- bs4 = "^0.0.2"
- psycopg2-binary = "^2.9.9"
- python-dotenv = "^1.0.1"
- gunicorn = "^22.0.0"


### Install

```bash
git clone https://github.com/StrangerAlien/page_analyzer

cd page_analyzer

make build
make start
```

### Для работы сервиса необходимы две переменные окружения:

- SECRET_KEY - со значением секрета для работы приложения.
- DATABASE_URL - путь к вашей подготовленной базе данных в виде унифицированного идентификатора ресурса (URI): 'postgresql://user:password@host:port/database_name'.



