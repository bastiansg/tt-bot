core-build:
	docker compose build tt-bot-core

core-run:
	docker compose run tt-bot-core


jupyter-build: core-build
	docker compose build tt-bot-jupyter

jupyter-run:
	docker compose up tt-bot-jupyter


app-build: core-build
	docker compose build tt-bot-app

app-run: app-build
	docker compose up tt-bot-app -d
