# -*- coding: utf-8 -*-

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
    web.run_app(app)
