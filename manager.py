from __future__ import unicode_literals, print_function, generators, division
import shelve

from model import Message


__author__ = 'pahaz'


# ===========================
#
#  [Mvc] 1.1 Model Manager
#
# ===========================


class MessageManager:
    def __init__(self, db_name):
        self._db = shelve.open(db_name)

    def all(self):
        messagers = []
        for id, data in self._db.items():
            m = Message(data['name'], data['message'])
            m.id = str(id)
            messagers.append(m)
        messagers.sort(key=lambda x: x.id)
        return messagers

    def save(self, message):
        data = {
            'message': message.message,
            'name': message.name,
        }

        if message.id:
            self._db[message.id] = data
        else:
            try:
                max_id = max(map(int, self._db.keys()))
            except ValueError:
                max_id = 1
            self._db[str(max_id + 1)] = data

        self._db.sync()

    def delete(self, message):
        if message.id:
            del self._db[message.id]
            self._db.sync()
            return True
        return False

    def filter_by_name(self, name):
        return [m for m in self.all() if m.name == name]

    def close(self):
        self._db.close()
