from typing import Callable, Dict, Type

from modules.redis.models import ParsedInstance

parsers: Dict[Type[ParsedInstance], Callable] = {}


def register(cls: Type[ParsedInstance]):
    def parser_decorator(parser):
        def wrapper(*args, **kwargs):
            return list(set(parser(*args, **kwargs)))

        if not parsers.get(cls):
            parsers[cls] = parser
        return wrapper

    return parser_decorator
