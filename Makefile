.PHONY: migrate build up down createsuperuser 

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

migrate:
	docker compose run --rm web python booksearch/manage.py migrate

createsuperuser:
	docker compose run --rm web python booksearch/manage.py createsuperuser