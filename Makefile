DOCKER_TEST=docker-compose -f deployment/docker-compose-test.yml
DOCKER_DEVELOPMENT=docker-compose -f deployment/docker-compose-development.yml
DOCKER_PROD=docker-compose -f deployment/docker-compose-production.yml -p "seats"

.PHONY: all
all: build

.PHONY: test
test:
	${DOCKER_TEST} build
	${DOCKER_TEST} run --rm api
	${DOCKER_TEST} down


.PHONY: build
build:
	docker build -t seats/python -f deployment/Dockerfile-python-base .
	docker build -t seats/api  -f deployment/Dockerfile-production .

.PHONY: start_prod
start_prod:
	${DOCKER_PROD} up -d

.PHONY: dev_stack
dev_stack:
	${DOCKER_DEVELOPMENT} up -d

.PHONY: run_server
run_server:
	python3 seats_api/manage.py runserver --settings=seats_api.settings_development


.PHONY: stop_dev_stack
stop_dev_stack:
	${DOCKER_DEVELOPMENT} down

.PHONY: update_requirements
update_requirements:
	./requirements/update.sh