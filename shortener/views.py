# -*- coding: utf-8 -*-

from time import time

from aiohttp import web

from shortener.utils import decode, encode


class Handler:
    def __init__(self, app):
        self._app = app

    async def generate(self, request):
        data = await request.post()
        long_url = data.get('url') or data.get('URL')
        keep_in_sec = data.get('keep_in_sec')

        if long_url is None:
            error = {'error': 'url is a required param'}
            return web.json_response(data=error, status=400)

        if keep_in_sec is None:
            keep_in_sec = self._app['config']['keep_in_sec']

        expires = int(time()) + int(keep_in_sec)

        res = await self._app['tarantool'].insert(
            self._app['config']['tarantool']['space'],
            (None, long_url, expires))
        idx, _, _ = res.data.pop()
        short_id = encode(idx)

        return web.json_response(
            data={
                'url': long_url,
                'short_url': 'https://%s/%s' % (request.url.host, short_id),
                'expires': expires
            },
            status=201)

    async def redirect(self, request):
        short_id = request.match_info['short_id']
        idx = decode(short_id)

        res = await self._app['tarantool'].select(
            self._app['config']['tarantool']['space'],
            idx)

        if not res.data:
            raise web.HTTPNotFound()

        _, url, _ = res.data.pop()
        return web.HTTPFound(location=url)
