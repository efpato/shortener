FROM tarantool/tarantool:1.10.2

LABEL maintainer="sergey.demenok@gmail.com"

WORKDIR /opt/tarantool

COPY *.lua /opt/tarantool/

EXPOSE 3301

CMD ["tarantool", "shortener.lua"]
