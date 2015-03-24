from __future__ import unicode_literals, print_function, generators, division

__author__ = 'pahaz'


class View:
    def __init__(self, template_name):
        self._template_name = template_name
        with open(self._template_name, 'rb') as f:
            template_bytes = f.read()
        self._template = template_bytes

    def render(self, **context):
        rendered = self._template
        for k, v in context.items():
            k = '{{' + k + '}}'
            if isinstance(v, str):
                v = v.encode()
            rendered = rendered.replace(k.encode(), v)
        return rendered


if __name__ == "__main__":
    view = View('main.html')
    assert isinstance(view._template, bytes)
    assert isinstance(view.render(), bytes)
    assert b'qwer' in view.render(messages="qwer"), "Problem in replace"
