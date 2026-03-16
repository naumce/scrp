FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8742

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8742"]
