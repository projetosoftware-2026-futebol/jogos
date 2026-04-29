FROM python:3.13-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache libpq

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/app

# CMD ["fastapi", "run", "app/main.py", "--port", "5000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["fastapi", "run", "app/main.py", "--port", "5000", "--proxy-headers"]
