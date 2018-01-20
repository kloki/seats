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

### test_data
```
python3 seats_api/manage.py loaddata example_event.json
```
This will create an event for testing. Will also create a super user with
the credentials admin:pass1234


## test

Will spin up everything in a docker environment.
Please make sure there are no conflicting docker images running.

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