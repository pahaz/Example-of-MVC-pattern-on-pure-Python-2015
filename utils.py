from urllib.parse import parse_qs


def parse_http_get_data(environ):
    return parse_qs(environ.get("QUERY_STRING", ""))


def parse_http_post_data(environ):
    """
    Parse a HTTP post data form WSGI `environ` argument.
    """
    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    request_body = environ["wsgi.input"].read(request_body_size)
    body_query_dict = parse_qs(request_body)

    return body_query_dict


def take_one_or_None(dict_, key):
    """
    Take one value by key from dict or return None.
        >>> d = {"foo":[1,2,3], "baz":7}
        >>> take_one_or_None(d, "foo")
        1
        >>> take_one_or_None(d, "bar") is None
        True
        >>> take_one_or_None(d, "baz")
        7
    """
    val = dict_.get(key)
    if type(val) in (list, tuple) and len(val) > 0:
        val = val[0]
    return val
