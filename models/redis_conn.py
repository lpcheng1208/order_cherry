# coding=utf-8
import os

import redis
import sys


sys.path.append('..')

m = redis.ConnectionPool(host='127.0.0.1', port=6380, password='123456', decode_responses=True)
rds_conn = redis.StrictRedis(connection_pool=m)