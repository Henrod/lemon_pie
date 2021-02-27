.PHONY: run
run:
	python app.py


.PHONY: venv
venv:
	pipenv shell

.PHONY: lint
lint:
	python -m flake8
	mypy --ignore-missing-imports lemon_pie


.PHONY: dev/ssl/create
dev/ssl/create:
	openssl req -x509 -out ../.cert/localhost.crt -keyout ../.cert/localhost.key \
		-newkey rsa:2048 -nodes -sha256 \
		-subj '/CN=localhost' -extensions EXT -config <( \
		printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
	sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ../.cert/localhost.crt

.PHONY: db/migrate
DATABASE_URL:=postgresql://admin:admin@localhost:5432/lemon_pie
db/migrate:
	psql $(DATABASE_URL) -f migrations/db.sql
