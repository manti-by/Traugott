start:
	docker-compose -f deploy/docker-compose.yml up -d

stop:
	docker-compose -f deploy/docker-compose.yml stop

destroy:
	docker-compose -f deploy/docker-compose.yml down

bash:
	docker exec -it django bash

build:
	docker build -f churchill/Dockerfile -t mantiby/churchill:latest .

pg_dump:
	pg_dump -U churchill -d churchill > database.sql

migrate:
	python manage.py migrate

static:
	python churchill/manage.py collectstatic --no-input

messages:
	python manage.py makemessages -a

check:
	black --target-version py38 churchill/
	isort churchill/*.py
	flake8
	standard --fix churchill/static/js/

test:
	pytest churchill/