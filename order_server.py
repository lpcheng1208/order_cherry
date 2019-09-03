#coding=UTF-8
import os.path
import logging
import logging.handlers
import json
from optparse import OptionParser
from apscheduler.scheduler import Scheduler
import cherrypy
# import snowflake.client
# from nsq.reader import Reader

import threading

from nsq.reader import Reader

import config
import urls
from views import nsq_worker
# from tasks import order_cherry, settle
import requests
from rc4 import rc4

from views.HelloWorld import HelloWordTest

version = '1.1.0'

# snowflake.client.setup(config.snowflake_host, config.snowflake_port)

def initLog(options):
    filename = options.logfile
    log_path = os.path.dirname(filename)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    logger = logging.getLogger()
    hdlr = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', backupCount=options.backupCount)
    formatter = logging.Formatter("[%(asctime)s]: %(filename)s:%(lineno)d %(levelname)s %(message)s" )
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    if options.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

def hex2str(s):
    if s[:2] == '0x' or s[:2] == '0X':
        s = s[2:]
    res = ""
    for i in range(0, len(s), 2):
        hex_dig = s[i:i + 2]
        res += (chr(int(hex_dig, base=16)))
    return res

    
def main():
    parser = OptionParser(usage="usage: python %prog [options] filename",
                          version="order_cherry server v%s" % version)
    parser.add_option("-p", "--port",
                      action="store",
                      type="int",
                      dest="port",
                      default=8060,
                      help="Listen Port")
    parser.add_option("-f", "--logfile",
                      action="store",
                      type="string",
                      dest="logfile",
                      default='./logs/run.log',
                      help="LogFile Path and Name. default=./run.log")
    parser.add_option("-n", "--backupCount",
                      action="store",
                      type="int",
                      dest="backupCount",
                      default=10,
                      help="LogFile BackUp Number")
    parser.add_option("-m", "--master",
                      action="store_true",
                      dest="master",
                      default=False,
                      help="master process")
    parser.add_option("-d", "--debug",
                          action="store_true",
                          dest="debug",
                          default=False,
                          help="debug mode")
    (options, args) = parser.parse_args()
    initLog(options)

    sched = Scheduler()
    # #定时任务
    # sched.add_cron_job(order_cherry.close_order, minute='*/2')
    #
    sched.start()

    cherrypy.config.update({'server.socket_host':'0.0.0.0',
                            'server.socket_port':8050,
                            'server.socket_queue_size':300,
                            'server.max_request_header_size':10 * 1024 * 1024,
                            'server.thread_pool':400,
                            'response.headers.Content-Type': 'application/json; charset=UTF-8',
                            'tools.encode.encoding': 'utf-8',
                            'engine.autoreload.on':True,
                            })
    cherrypy.tree.mount(urls.HellowWord(), '/v1/2')
    cherrypy.tree.mount(urls.Test(), '/api')
    cherrypy.tree.mount(HelloWordTest(), '/hello')
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    main()
