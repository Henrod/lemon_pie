FROM python:3.7-slim

WORKDIR /app
ENV APP_VERSION="0.0.2"
ENV WHL_FILE="lemon_pie-${APP_VERSION}-py3-none-any.whl"

RUN python -m pip install pipenv

COPY app.py .
COPY Pipfile* .
COPY dist/${WHL_FILE} .

RUN pipenv install ${WHL_FILE}
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "app.py"]
