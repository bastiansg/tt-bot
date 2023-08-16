include .env
export $(shell sed 's/=.*//' .env)


core-build:
	[ -e .secrets/.env ] || touch .secrets/.env
	docker compose build tt-bot-core

core-run:
	docker compose run tt-bot-core


app-build: core-build
	docker compose build tt-bot-app

app-run: app-build mongo-start
	docker compose run tt-bot-app

app-up: app-build mongo-start
	docker compose up tt-bot-app -d

app-stop:
	docker compose stop tt-bot-app


mongo-start:
	docker compose up -d tt-bot-mongo

mongo-stop:
	docker compose stop tt-bot-mongo

mongo-cache-flush:
	docker compose exec tt-bot-mongo mongosh $(CACHE_DB) --eval "db.dropDatabase();" > /dev/null
