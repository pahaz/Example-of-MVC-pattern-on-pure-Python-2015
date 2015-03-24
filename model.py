from __future__ import unicode_literals, print_function, generators, division

__author__ = 'pahaz'


class Message:
    def __init__(self, name, message):
        self.message = message
        self.name = name
        self.id = None
