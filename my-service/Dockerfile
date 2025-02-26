# Please fill in Dockerfile content
# --- Stage 1: Builder Image ---
FROM python:3.12 AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  build-essential \ 
  python3-dev \      
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN poetry build

# --- Stage 2: Runtime Image ---
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /app/dist/*.whl ./dist/
COPY --from=builder /app/my_service ./my_service

RUN pip install --no-cache-dir ./dist/*.whl

CMD ["uvicorn", "my_service.main:app", "--host", "0.0.0.0", "--port", "9000"]