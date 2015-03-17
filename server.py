from wsgiref.simple_server import make_server
from wsgi import application

print('Listen: http://127.0.0.1:8001/')
httpd = make_server('', 8001, application)
httpd.serve_forever()
