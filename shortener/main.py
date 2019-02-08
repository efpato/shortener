# -*- coding: utf-8 -*-

import pathlib

import aiotarantool
from aiohttp import web

from shortener.routes import setup_routes
from shortener.utils import load_config
from shortener.views import Handler


PROJ_ROOT = pathlib.Path(__file__).parent.parent


def setup_tarantool(app):
    tarantool = aiotarantool.connect(
        app['conf']['tarantool']['host'],
        app['conf']['tarantool']['port'],
        user=app['conf']['tarantool']['user'],
        password=app['conf']['tarantool']['password'])

    async def close_tarantool(app):
        app['tarantool'].close()

    app.on_cleanup.append(close_tarantool)
    app['tarantool'] = tarantool

    return tarantool


app = web.Application()
app['conf'] = load_config(PROJ_ROOT / 'config' / 'config.yml')
handler = Handler(app)
setup_routes(app, handler)
setup_tarantool(app)


if __name__ == '__main__':
    web.run_app(app, host=app['conf']['app']['host'],
                port=app['conf']['app']['port'])
