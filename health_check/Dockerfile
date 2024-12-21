# Stage 1
FROM python:3.11.0-alpine AS base
WORKDIR /app
RUN apk add gcc python3-dev musl-dev linux-headers --no-cach
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev


# Stage 2
FROM base AS builder
COPY . /app

# Stage 3
FROM python:3.11.0-alpine AS runtime
WORKDIR /app

COPY --from=base /usr/local/bin/poetry /usr/local/bin/poetry
COPY --from=base /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /app /app
EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
