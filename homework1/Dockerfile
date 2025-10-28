# build-env
FROM python:3.12-slim AS build-env

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./

ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync

# build-app
FROM python:3.12-slim 

WORKDIR /app

ENV PATH="/root/.local/bin:${PATH}"

COPY --from=build-env /root/.local /root/.local
COPY --from=build-env /app/.venv /app/.venv

COPY src ./src
COPY model ./model
COPY main.py ./main.py

EXPOSE 8000

CMD ["uv", "run", "main.py"]

# 1.61GB -> 1.33GB