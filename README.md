# api seats

please install docker and docker-compose before continuing.

## development setup

### Setup virtualenv

```
virtualenv env -p python3
source env/bin/activate
pip install -r requirements/production.txt
```

### start database

```
make dev_stack
```

### Start services

```
make dev_stack
```
### Migrate
```
python3 seats_api/manage.py migrate
```

### Start dev instance

```
make runserver
```

## test

Will spin everything in an docker environment.
Please make sure there are no conflicting docker images

```
make test
```

### Prod

```
make build
make start_prod
```

### if needed run migrations

```
docker exec seats_api_1 python3 manage.py migrate
```