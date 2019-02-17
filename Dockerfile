FROM python:3.7-stretch

LABEL maintainer="sergey.demenok@gmail.com"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY config /app/config
COPY shortener /app/shortener

EXPOSE 8080

ENTRYPOINT ["python", "-m", "shortener.main", "-a", "0.0.0.0", "-p", "8080"]

