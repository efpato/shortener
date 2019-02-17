# -*- coding: utf-8 -*-

import argparse

import aiotarantool
from aiohttp import web

from shortener.routes import setup_routes
from shortener.settings import config
from shortener.views import Handler


def setup_tarantool(app):
    tarantool = aiotarantool.connect(
        app['config']['tarantool']['host'],
        app['config']['tarantool']['port'],
        user=app['config']['tarantool']['user'],
        password=app['config']['tarantool']['password'])

    async def close_tarantool(app):
        await app['tarantool'].close()

    app.on_cleanup.append(close_tarantool)
    app['tarantool'] = tarantool

    return tarantool


app = web.Application()
app['config'] = config
handler = Handler(app)
setup_routes(app, handler)
setup_tarantool(app)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Link shortener")
    parser.add_argument('-a', '--address',
                        help='binding address',
                        default='127.0.0.1')
    parser.add_argument('-p', '--port',
                        help='binding port',
                        default=8080)
    args = parser.parse_args()
    web.run_app(app, host=args.address, port=args.port)
