# coding=UTF-8
import cherrypy
import logging
import functools
# from hashlib import md5
# import time
# import datetime
# import json
# import random
# import os
# from models.redis_conn import redisconn
import config
# from views import activity, pay, redis_const
# from tasks import settle
from models.redis_conn import rds_conn
from utils.tools import json_encoder

def exp(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            logging.info("kwargs %s" % kwargs)
            logging.info("request.path:%s%s kwargs %s" % (cherrypy.request.script_name, cherrypy.request.path_info, kwargs))
            return method(*args, **kwargs)
        except:
            logging.error("api error: %s" % method.__name__, exc_info=True)
            return {"code":500, "desc":"系统异常"}
    return wrapper

class HellowWord():
    @exp
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def v1(self, **kwargs):
        return {"code": 0,  "msg": "succuse", "data": {}}


class Test():
    @exp
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def v1(self, **kwargs):
        rds_conn.set("bbb", 1)
        a = rds_conn.get("bbb")
        return {"code": 0, "msg": "succuse", "data": {"a": 1, "aaa": rds_conn.get("bbb")}}