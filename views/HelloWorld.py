import logging

import cherrypy

from handlers.hellow import test
from views.Base import ApiResult, exp


class HelloWordTest(ApiResult):
    @exp
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def v1(self, **kwargs):
        result = self.get_inst()
        data = test()
        return result.success(data=data)