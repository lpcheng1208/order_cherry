# coding=UTF-8
import cherrypy
import logging
import functools


def exp(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            logging.info("kwargs %s" % (kwargs))
            logging.info("request.path:%s%s kwargs %s" % (cherrypy.request.script_name, cherrypy.request.path_info, kwargs))
            return method(*args, **kwargs)
        except:
            logging.error("api error: %s" % method.__name__, exc_info=True)
            return {"code":500, "desc":"系统异常"}
    return wrapper


class ApiResult(dict):


    def error(self, code=6001, msg="", data={}):
        self["code"] = code
        self["msg"] = msg
        self["data"] = data
        logging.info("data: %s" % self)
        return self


    def success(self, code=0, data={}, msg="success"):
        self["code"] = code
        self["msg"] = msg
        self["data"] = data
        logging.info("data: %s" % self)
        return self

    @classmethod
    def get_inst(cls):
        return ApiResult(code=0, msg="", data={})