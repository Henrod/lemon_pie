.PHONY: venv
venv:
	pipenv shell

.PHONY: dev/run
dev/run:
	LEMON_PIE_PASSWORD=admin python app.py \
	--env development \
	--debug true \
	--start_vote_time 09:00 \
	--end_vote_time 16:00

.PHONY: dev/deps
dev/deps:
	docker compose -p lemon_pie up -d

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
