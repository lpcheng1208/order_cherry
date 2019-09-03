#!/usr/bin/env python
# coding=UTF-8
import json
import datetime
import calendar
import decimal
import random

def hex2str(s):
    if s[:2] == '0x' or s[:2] == '0X':
        s = s[2:]
    res = ""
    for i in range(0, len(s), 2):
        hex_dig = s[i:i + 2]
        res += (chr(int(hex_dig, base=16)))
    return res

def str2hex(string):
    res = ""
    for s in string:
        hex_dig = hex(ord(s))[2:]
        if len(hex_dig) == 1:
            hex_dig = "0" + hex_dig
        res += hex_dig
    return res

def create_order_no():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    randstr = str(random.randint(1000, 9999))
    return now + randstr

def json_encoder(data):
    return json.dumps(data, cls=DateEncoder)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return str(obj.quantize(decimal.Decimal('0.00')))
        else:
            return json.JSONEncoder.default(self, obj)


_MONTH = ((0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
          (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31))


def get_date(d=0, m=0, y=0, start_date=None, format=""):
    if not start_date:
        start_date = datetime.datetime.now()
    if d != 0:
        start_date += datetime.timedelta(days=d)
    if not (y or m):
        if format == "date":
            return start_date.strftime("%Y-%m-%d")
        elif format == "date_time":
            return start_date.strftime("%m月%d日")
        return start_date.strftime("%Y-%m-%d %H:%M:%S")

    n = int(start_date.year) * 12 + int(start_date.month) - 1
    n = n + m
    ryear = n / 12
    rmonth = n % 12 + 1
    rday = start_date.day
    if calendar.isleap(ryear):
        if rday > _MONTH[1][rmonth]:
            rday = _MONTH[1][rmonth]
    else:
        if rday > _MONTH[0][rmonth]:
            rday = _MONTH[0][rmonth]

    y += (m + int(start_date.month) - 1) / 12
    result = start_date.replace(year=start_date.year + y, month=rmonth, day=rday)
    if format == "date":
        return result.strftime("%Y-%m-%d")
    elif format == "date_time":
        return start_date.strftime("%m月%d日")
    return result.strftime("%Y-%m-%d %H:%M:%S")