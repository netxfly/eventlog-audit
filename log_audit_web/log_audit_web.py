# -*- coding:utf8 -*-
import os, sqlite3
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import define, options

from config import *
from router import *

#继承自tornado.web.Application类
#---------------------------------------------------------------------------
class Application(tornado.web.Application):
    def __init__(self):
        handlers = routers
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = sqlite3.connect(options.dbName)

#---------------------------------------------------------------------------
#首页面
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        page = self.get_argument("page", "") or 1
        page = int(page)

        cu = self.application.db.cursor()
        sql = "select distinct(log_type) from eventlog"
        cu.execute(sql)
        log_types = cu.fetchall()

        log_summer = {}
        for item in log_types:
            sql = "select count(1) from eventlog where log_type = '%s'" % item
            cu.execute(sql)
            ret = cu.fetchall()
            log_summer[item] = ret

        print log_summer

        pagesize = 200
        sql = "select count(1) from eventlog"
        cu.execute(sql)
        total_size = cu.fetchall()[0][0]
        print "total_size : %s" % total_size, type(total_size)

        if total_size % pagesize == 0:
            pages = total_size / pagesize / 2
        else:
            pages = total_size / pagesize / 2 + 1

        if page > pages:
            page = pages

        if page < 1 :
            page = 1

        i = (page - 1) * pagesize
        if i < 0:
            i = 0

        sql = "select * from eventlog limit %s, %s" % (i, pagesize)
        cu.execute(sql)
        log_info = cu.fetchall()

        self.render("home.html", log_summer=log_summer, log_types=log_types, log_info=log_info,
            page=page, pages=pages)


    def post(self):
        pass


#---------------------------------------------------------------------------
#根据日志类型展示
class log_type(tornado.web.RequestHandler):
    def get(self):
        page = self.get_argument("page", "") or 1
        page = int(page)
        log_type = self.get_argument("log_type", "") or "Information"

        cu = self.application.db.cursor()
        sql = "select distinct(log_type) from eventlog"
        cu.execute(sql)
        log_types = cu.fetchall()

        log_summer = {}
        for item in log_types:
            sql = "select count(1) from eventlog where log_type = '%s'" % item
            cu.execute(sql)
            ret = cu.fetchall()
            log_summer[item] = ret

        print log_summer

        pagesize = 200
        sql = "select count(1) from eventlog where log_type = '%s'" % log_type
        cu.execute(sql)
        total_size = cu.fetchall()[0][0]
        print "total_size : %s" % total_size, type(total_size)

        if total_size % pagesize == 0:
            pages = total_size / pagesize / 2
        else:
            pages = total_size / pagesize / 2 + 1

        if page > pages:
            page = pages

        if page < 1 :
            page = 1

        i = (page - 1) * pagesize
        if i < 0:
            i = 0

        sql = "select * from eventlog where log_type = '%s' limit %s, %s" % (log_type, i, pagesize)
        cu.execute(sql)
        log_info = cu.fetchall()

        self.render("log_type.html", log_summer=log_summer, log_types=log_types, log_info=log_info,
            page=page, pages=pages, log_type=log_type)


    def post(self):
        pass
#---------------------------------------------------------------------------
#主函数
def main():
    app = Application()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
