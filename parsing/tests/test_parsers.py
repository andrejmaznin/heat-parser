import asyncio

from redis import Redis

from modules.redis.models import Email
from parsing.parsers import parse_recursive

r = Redis()


def test_all_parsers():
    asyncio.run(
        parse_recursive(
            entrypoint='https://www.verstov.info/',
            depth=2,
            ignore_local=False
        )
    )


print([Email.get(pk).__dict__ for pk in Email.all_pks()])
print(len(r.lrange('mymodel.Email', 0, -1)))
