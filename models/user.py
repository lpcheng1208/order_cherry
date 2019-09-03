#!/usr/bin/env python
# coding=UTF-8
import time
import datetime
from models.dao import BaseDB

class UserInfo(BaseDB):
    def get_user_info(self, ACCOUNT_ID, STATUS=1):
        sql = "SELECT * FROM user_info WHERE ACCOUNT_ID='%s' AND `STATUS`='%s'" % (ACCOUNT_ID, STATUS)
        return self.get(sql)
    
    