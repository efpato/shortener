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
$ # generate short link (expires in 7 days by default)
$ curl -XPOST -u user:password -d url=http://ya.ru http://localhost/generate_short_link
$ # generate short link (expires in 30 seconds)
$ curl -XPOST -u user:password -d url=http://google.com -d keep_in_sec=30 http://localhost/generate_short_link
$ # redirect short link
$ curl -L http://localhost/a
```

* stop
```bash
$ docker-compose down
```
