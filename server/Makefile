.PHONY: venv
venv:
	pipenv shell

.PHONY: dev/run
dev/run:
	LEMON_PIE_PASSWORD=admin python app.py \
	--env development \
	--debug true \
	--end_vote_time 23:59

.PHONY: prod/run
prod/run:
	python app.py \
	--env production \
	--cert ../.cert/localhost.crt \
	--key ../.cert/localhost.key \
	--debug true

.PHONY: db/start
db/start:
	docker compose up -d

.PHONY: db/migrate
DATABASE_URL:=postgresql://admin:admin@localhost:5432/lemon_pie
db/migrate:
	psql $(DATABASE_URL) -f migrations/db.sql

.PHONY: lint
lint:
	python -m flake8
	mypy --ignore-missing-imports --disallow-untyped-defs .


.PHONY: docker/build
docker/build:
	python setup.py bdist_wheel
	docker build -t lemon_pie -f Dockerfile .
