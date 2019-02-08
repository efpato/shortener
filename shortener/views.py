# -*- coding: utf-8 -*-

from time import time

from aiohttp import web

from shortener.utils import decode, encode


class Handler:
    def __init__(self, app):
        self._app = app

    async def generate(self, request):
        data = await request.post()
        long_url = data.get('url', None)

        if long_url is None:
            error = {'error': 'url is a required param'}
            return web.json_response(data=error, status=400)

        res = await self._app['tarantool'].insert(
            self._app['conf']['tarantool']['space'],
            (None, long_url, time()))
        idx, _, _ = res.data.pop()
        short_id = encode(idx)

        return web.json_response(
            data={'url': long_url,
                  'short_url': '%s%s' % (request.url, short_id)},
            status=201)

    async def redirect(self, request):
        short_id = request.match_info['short_id']
        idx = decode(short_id)

        res = await self._app['tarantool'].select(
            self._app['conf']['tarantool']['space'],
            idx)

        if not res.data:
            raise web.HTTPNotFound()

        _, url, _ = res.data.pop()
        return web.HTTPFound(location=url)
