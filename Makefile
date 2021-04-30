build:
	docker build -t mantiby/churchill:latest .

migrate:
	docker exec -it churchill-django python manage.py migrate

static:
	docker exec -it churchill-django python manage.py collectstatic --no-input

bash:
	docker exec -it churchill-django bash

update-db:
	scp amon-ra:/home/manti/www/churchill.manti.by/data/db.sqlite3 /home/manti/www/churchill/db.sqlite3

check:
	flake8 churchill/
	black --target-version py38 churchill/
	standard --fix churchill/static/js/

test:
	pytest churchill/
