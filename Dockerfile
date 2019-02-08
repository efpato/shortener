FROM python:3.7-stretch

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY config /app/config
COPY shortener /app/shortener

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--bind", ":8000", "--workers", "3", "--worker-class", "aiohttp.worker.GunicornWebWorker", "shortener.main:app"]

