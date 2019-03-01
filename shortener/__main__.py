# -*- coding: utf-8 -*-

import argparse
import logging

import aiotarantool
from aiohttp import web
from aiohttp_basicauth_middleware import basic_auth_middleware, BaseStrategy

from shortener.routes import setup_routes
from shortener.utils import load_config
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


def main():
    parser = argparse.ArgumentParser(
        prog='shortener', description='Link shortener')
    parser.add_argument(
        '-c', '--config', help='path to the config file', required=True)
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except IOError:
        parser.error('config file "%s" not found or unreadable' % args.config)

    logging.basicConfig(
        level=logging.getLevelName(config['logging']['level'].upper()),
        format=config['logging']['format'])

    app = web.Application()
    app['config'] = config
    handler = Handler(app)
    setup_routes(app, handler)
    setup_tarantool(app)
    app.middlewares.append(
        basic_auth_middleware(['/generate_short_link'],
                              {config['user']: config['password']},
                              BaseStrategy))

    web.run_app(app, host=config['addr'], port=config['port'])


if __name__ == '__main__':
    main()
