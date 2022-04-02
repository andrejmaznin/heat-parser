import asyncio

from modules.redis.models import Email
from parsing.parsers import parse_recursive


def test_all_parsers():
    asyncio.run(
        parse_recursive(
            entrypoint='https://www.verstov.info/',
            depth=2,
            ignore_local=False
        )
    )


print(set([Email.get(pk).email for pk in Email.all_pks()]))
test_all_parsers()
