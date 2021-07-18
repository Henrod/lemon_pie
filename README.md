# LemonPie

Judge your friends using emojis 😈

## Local development

### Start the server

```shell
cd server

# Start virtual environment
make venv

# Create self-signed certificate for local development
# and add it as trusted root certificate.
# Works only for MacOS.
make dev/ssl/create

make run
```

### Start the UI

```shell
cd client
npm start
```

## Next steps

### Product

- [ ] Enable voting depending on the time of the day
- [ ] Custom emojis - changeble from an endpoint
- [ ] Force voting in everyone or no one
- [ ] "How it works" page

### Technical

- [ ] SSL connection
- [ ] Access the API from outside the browser (e.g. curl)
- [ ] Database migrations
- [ ] Local development without login
- [ ] Automated tests

## Why LemonPie?

Torta de climão 🍰😭
