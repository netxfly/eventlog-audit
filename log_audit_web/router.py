# -*- coding:utf8 -*-

#导入模块中的各个类
from log_audit_web import *


#------------------------------------------------------------------------
#路由配置
routers = [
        (r"/", MainHandler),
        (r"/log_type/", log_type),
        ]

settings = dict(
        	template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = False,
            cookie_secret = "www.xsec.io"
            )
