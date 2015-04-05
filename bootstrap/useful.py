#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import sqlite3
import json

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def getTweetsFromDB(substring='', latest=0, hours = 0, month = 0):
    if latest: con = sqlite3.connect('var/www/tweets.db')
    else : con = sqlite3.connect('var/www/alltweets.db')
    #print type(substring)
    query = "SELECT * from tweets"
    if substring:
        query += " WHERE content_lower LIKE '%%%s%%'"%substring
    if latest:
        query += " ORDER BY created_at DESC LIMIT %i" % latest
    #print query
    data = pd.read_sql(query,con)
    data = data.sort('created_at')

    if hours:
        data.index = [data.hourly, data.index]
        json = list()
        for hour in data.index.levels[0][-hours:]:
          json.append("""{"date":"%s","tweets":%s}""" % (hour,data.loc[hour].to_json(orient = 'records', date_format = 'iso')))
          json = ",".join(json)
          con.close()
          del data
          return '[%s]' % json

    if month:
        data = data.loc[data.month == month]
        data.index = [data.day, data.index]
        json = list()
        for day in data.index.levels[0]:
            json.append("""{"date":"%i","tweets":%s}""" % (day,data.loc[day].to_json(orient = 'records', date_format = 'iso')))
        json = ",".join(json)
        con.close()
        del data
        return '[%s]' % json

    else: return data.to_json(orient = 'records', date_format = 'iso')
