from typing import Callable, Dict

parsers: Dict[str, Callable] = {}


def register(name):
    def parser_decorator(parser):
        def wrapper(*args, **kwargs):
            return list(set(parser(*args, **kwargs)))

        if not parsers.get(name):
            parsers[name] = parser
        return wrapper

    return parser_decorator
