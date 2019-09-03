#!/usr/bin/env python
# coding=UTF-8
import time
import datetime
from models.user import UserInfo

class Order(UserInfo):
    
    def get_merchant(self, merchant_id):
        sql = "SELECT * FROM merchant WHERE ID=%s" % merchant_id
        return self.get(sql)



