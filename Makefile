DOCKER_CMD=docker exec -it agenda_api

_config-env:
	[ -f .env ] || cp .env.sample .env

_upgrade-pip:
	${DOCKER_CMD} pip install --upgrade pip

build: _config-env
	docker-compose up -d

setup: _upgrade-pip
	${DOCKER_CMD} pip install -r requirements-dev.txt

flake8:
	${DOCKER_CMD} black .
	${DOCKER_CMD} flake8 --exclude=migrations,tests .

migrate-init:
	${DOCKER_CMD} python api/manage.py db init

migrate:
	${DOCKER_CMD} python api/manage.py db migrate

migrate-apply:
	${DOCKER_CMD} python api/manage.py db upgrade

downgrade:
	${DOCKER_CMD} python api/manage.py db downgrade -1

start:
	${DOCKER_CMD} python api/app.py


