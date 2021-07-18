.PHONY: venv
venv:
	pipenv shell

.PHONY: run
dev/run:
	python app.py \
	--cert ../.cert/localhost.crt \
	--key ../.cert/localhost.key \
	--env development \
	--debug true

.PHONY: dev/ssl/create
dev/ssl/create:
	@echo "creating self-signed certificate for development purposes"
	openssl req -x509 -out ../.cert/localhost.crt -keyout ../.cert/localhost.key \
		-newkey rsa:2048 -nodes -sha256 \
		-subj '/CN=localhost' -extensions EXT -config <( \
		printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
	@echo "adding self-signed certificates as trusted to CA"
	sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ../.cert/localhost.crt

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
	mypy --ignore-missing-imports lemon_pie


.PHONY: prod/build
prod/build:
	cd ../client/lemon_pie && npm run build
	cp -r ../client/lemon_pie/build lemon_pie
