FROM python:3.11-slim

RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt gunicorn

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

CMD ["gunicorn", "main:app", "--workers", "2", "--bind", "0.0.0.0:8000", "--timeout", "0", "-k", "uvicorn.workers.UvicornWorker", "--log-level", "debug"]