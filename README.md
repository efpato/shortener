shortener
=========

Python link shortener

### Usage

* build
```bash
$ docker-compose build
```

* start
```bash
$ docker-compose up -d
$ # generate short link
$ curl -XPOST -F 'url=http://ya.ru' http://localhost/
$ # redirect short link
$ curl -L http://localhost/a
```

* stop
```bash
$ docker-compose down
```
