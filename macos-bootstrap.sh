poetry install
docker run -p 6379:6379 --name redis-redisjson redislabs/rejson:latest
