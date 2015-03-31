from __future__ import unicode_literals, print_function, generators, division

__author__ = 'pahaz'


class Router:
    def __init__(self):
        self._routs = {}

    def add_route(self, url, controller):
        self._routs[url] = controller

    def resolve(self, url):
        callback = self._routs.get(url)
        if callback:
            return callback
        return self.default_route

    def default_route(self, *args, **kwargs):
        status = '404 Not Found'
        body = b''
        return status, body
# some
# some!
