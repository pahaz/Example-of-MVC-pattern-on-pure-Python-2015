from __future__ import unicode_literals, print_function, generators, division
import re

__author__ = 'pahaz'


# ===========================
#
# [mVc] 2.0 View
#
# ===========================

EXPR_PATTERN = b'{{ (?P<EXPR_expr>.+?) }}'
FOR_BLOCK_PATTERN = b'{% for (?P<FOR_var>[a-zA-Z0-9]+?) in ' \
                    b'(?P<FOR_iter_expr>.+?) %}(?P<FOR_body>.+){% endfor %}'
IF_BLOCK_PATTERN = b'{% if (?P<IF_expr>.+?) %}(?P<IF_expr_true>.+?)' \
                   b'(?:{% else %}(?P<IF_expr_false>.+?))?{% endif %}'


def _IF_BLOCK(context, callback, expr, expr_true, expr_false):
    expr = eval(expr, None, context)
    if expr:
        return callback(expr_true, context)
    else:
        return callback(expr_false, context)


def _FOR_BLOCK(context, callback, var, iter_expr, body):
    var = var.decode()
    results = []
    iterable = eval(iter_expr, None, context)
    for val in iterable:
        context[var] = val
        result = callback(body, context)
        results.append(result)
    return b''.join(results)


def _EXPR_BLOCK(context, callback, expr):
    result = eval(expr, None, context)
    return result


BLOCK_SPECIFICATION = [
    (b'FOR', FOR_BLOCK_PATTERN.replace(b' ', b'\\s*')),
    (b'IF', IF_BLOCK_PATTERN.replace(b' ', b'\\s*')),
    (b'EXPR', EXPR_PATTERN.replace(b' ', b'\\s*')),
    (b'OTHER', b'.+?'),  # Any other character
]

BLOCK_REGEXP = b'|'.join(
    b'(?P<' + pair[0] + b'>' + pair[1] + b')' for pair in BLOCK_SPECIFICATION
)


def render_template_byres(template, context):
    tkns = list(re.finditer(BLOCK_REGEXP, template, re.MULTILINE | re.DOTALL))
    results = []
    for token in tkns:
        if token.lastgroup != 'OTHER':
            kwargs = {k[len(token.lastgroup) + 1:]: v for k, v in
                      token.groupdict().items()
                      if k.startswith(token.lastgroup + '_')}
            try:
                result = globals()['_' + token.lastgroup + '_BLOCK'](
                    context, render_template_byres, **kwargs)
                if not isinstance(result, bytes):
                    result = str(result).encode()
            except Exception as e:
                result = b''.join([b"<span style='color: red' class='error'>",
                                   str(e).encode(),
                                   b"</span>"])
        else:
            result = token.group(token.lastgroup)
        results.append(result)
    return b''.join(results)


class View:
    def __init__(self, template_name):
        self._template_name = template_name
        with open(self._template_name, 'rb') as f:
            template_bytes = f.read()
        self._template = template_bytes

    def render(self, **context):
        rendered = self._template
        return render_template_byres(rendered, context)


if __name__ == "__main__":
    a = open('main.html', 'rb').read()
    z = render_template_byres(
    b"{% for x in range(length) %}{{ x }},{% endfor %}",
        {'length': 4})
    assert z == b'0,1,2,3,', "Bad render_template_byres()"
    z = render_template_byres(
        b"{{x }} {{y}} {{z}}",
        {'x': 4, 'y': 'q', 'z': b'4'})
    assert z == b'4 q 4', "Bad render_template_byres()"

    view = View('main.html')
    assert isinstance(view._template, bytes)
    assert isinstance(view.render(), bytes)
