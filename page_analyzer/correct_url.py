from urllib.parse import urlparse

import validators


def correct_url(url):
    errors = []
    parsed_url = urlparse(url)

    if all([parsed_url.scheme, parsed_url.netloc]) and len(url) > 255:
        errors.append('URL превышает 255 символов')
    if validators.url(url) is not True:
        errors.append('Некорректный URL')
    return errors
