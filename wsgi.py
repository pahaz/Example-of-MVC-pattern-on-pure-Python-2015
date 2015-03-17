from utils import parse_http_post_data, take_one_or_None, parse_http_get_data


data_messages = [
    b'Name: user<br>Message: hi!',
    b'Name: user<br>Message: hi!',
]


def application(environ, start_response):
    REQUEST_METHOD = environ['REQUEST_METHOD']
    POST = parse_http_post_data(environ)
    GET = parse_http_get_data(environ)
    # print(REQUEST_METHOD)
    # print(GET)
    # print(POST)

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    with open('main.html', 'rb') as f:
        template_bytes = f.read()

    if REQUEST_METHOD == 'POST':
        status = '303 See Other'
        headers.append(('Location', '/'))
        name = take_one_or_None(POST, b'name')
        message = take_one_or_None(POST, b'message')
        data_messages.append(b"Name: " + name + b"<br>Message: " + message)
        start_response(status, headers)
        return [b'']

    messages = b'<hr>'.join(data_messages)
    template_bytes = template_bytes.replace(b'{{messages}}', messages)

    start_response(status, headers)
    return [template_bytes]
