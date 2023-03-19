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
	${DOCKER_CMD} black
	${DOCKER_CMD} flake8

start:
	${DOCKER_CMD} python api/app.py
