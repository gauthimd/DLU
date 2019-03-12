#!/usr/bin/python3
# -*- coding: utf-8 -*-

from application.app import create_app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from application.config import instance_config

app = create_app(instance_config)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
