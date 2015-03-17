from urllib.parse import parse_qs
from utils import parse_http_post_data, take_one_or_None


data_messages = [
    b'Name: user<br>Message: hi!',
    b'Name: user<br>Message: hi!',
]


def application(environ, start_response):
    REQUEST_METHOD = environ['REQUEST_METHOD']

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    with open('main.html', 'rb') as f:
        template_bytes = f.read()


    if REQUEST_METHOD == 'POST':
        post = parse_http_post_data(environ)
        name = take_one_or_None(post, b'name')
        message = take_one_or_None(post, b'message')
        data_messages.append(b"Name: " + name + b"<br>Message: " + message)
        start_response(status, headers)
        return [b'<script>window.location.href = "/";</script>']
    else:
        post = []

    messages = b'<hr>'.join(data_messages)
    template_bytes = template_bytes.replace(b'{{messages}}', messages)

    start_response(status, headers)
    return [template_bytes, b'<hr>', repr(post).encode('utf-8')]
