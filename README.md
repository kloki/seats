# api seats

An swagger schema is available at http://127.0.0.1:8000/schema/ when
running dev environment.

## Adding a group
The add group endpoint is a bit rushed so it doesn't play nice with swagger
Here is how to use:

```
curl -H "Content-Type: application/json" -X POST -d '{"event":1,"guests":["name1","name2"]',"section":1} http://127.0.0.1:8000/api/add-group/
```
event and section are pk's and section is optional.

# Setup

please install docker and docker-compose before continuing. If you dont want to user docker make sure a postgres instance is running on 0.0.0.0:5432.

## development setup

### Setup virtualenv

```
virtualenv env -p python3
source env/bin/activate
pip install -r requirements/production.txt
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
This will create an event for testing. Will also create a super user with
the credentials admin:pass1234

```
python3 seats_api/manage.py loaddata example_event.json
```

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
