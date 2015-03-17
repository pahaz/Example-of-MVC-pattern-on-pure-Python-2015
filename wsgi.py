data_messages = [
    b'Name: user<br>Message: hi!',
    b'Name: user<br>Message: hi!',
]


def application(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/html; charset=utf-8')] # HTTP Headers
    with open('main.html', 'rb') as f:
        template_bytes = f.read()
    messages = b'<hr>'.join(data_messages)
    template_bytes.replace(b'{{messages}}', messages)
    start_response(status, headers)
    return [template_bytes]
