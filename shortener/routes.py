# -*- coding: utf-8 -*-


def setup_routes(app, handler):
    app.router.add_post('/generate_short_link', handler.generate)
    app.router.add_get('/{short_id}', handler.redirect)
