FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./

RUN echo $PATH
ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync

COPY src ./src

 # should it be there??
COPY models ./models

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]