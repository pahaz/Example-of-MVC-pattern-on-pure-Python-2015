messages = [
    b'Name: Pavel<br>Message: hi!!',
    b'Name: Vasya<br>Message: How do you do...',
]


def application(env, callback):
    global messages

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]

    msgs = b'<hr>'.join(messages)

    with open('main.html', 'rb') as f:
        text_bytes = f.read().replace(b'{{messages}}', msgs)

    callback(status, headers)
    return [text_bytes]
