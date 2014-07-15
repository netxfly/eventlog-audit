# -*- coding:utf8 -*-
from tornado.options import define, options

#服务器配置项
define("port", default=9999, help="run on the given port", type=int)
define("dbName", default="Eventlog.db", help="database name")

