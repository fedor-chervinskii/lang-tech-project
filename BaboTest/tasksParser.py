#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymorphy2
from collections import OrderedDict
import requests
import json
from math import sqrt

def getAllVersionOfKeywords(keywords, morph):
    searchKeywords = []

    for keyword in keywords:
        for parsedWord in morph.parse(keyword):
            if parsedWord.tag.POS == 'NOUN':
                for lexeme in parsedWord.lexeme:
                    searchKeywords.append(lexeme.word)

    #Leave only unique words
    return list(OrderedDict.fromkeys(searchKeywords))

def getTweetRelevance(task, tweet):

    if len(tweet.apilocation) > 0:
        print sqrt((tweet.apilocation['lat']-task['location']['lat'])**2 + (tweet.apilocation['lng']-task['location']['lon'])**2)

    tokenizedTask = frozenset(task['taskInfo']['searchKeywords'])
    tokenizedTweet = frozenset(tweet.text.split(' '))
    #print tokenizedTask.intersection(tokenizedTweet)

    return len(tokenizedTask.intersection(tokenizedTweet))

def parseTask(task):
    #Reading a list of stop words
    f = open('prepositions.csv')
    preps = [unicode(line[:-1].decode('utf-8')) for line in f.readlines()]

    #Initializing morph amalyzer to get all the forms of a word
    morph = pymorphy2.MorphAnalyzer()

    taskInfo = {}

    tokenizedTask = task['text'].split(' ')
    #All the keywords are after some common text that ends with 'за'
    keywords = tokenizedTask[tokenizedTask.index(u'за') + 1:]

    keywords = [k for k in keywords if not k in preps]
    taskInfo['keywords'] = keywords

    taskInfo['searchKeywords'] = getAllVersionOfKeywords(keywords, morph)
    task["taskInfo"] = taskInfo
    #Print it out
    print '%i keywords' % len(taskInfo['searchKeywords'])

    return taskInfo

def getLocationCoordinates(location):
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json',
                        params={'address' : location,
                                'key' : 'AIzaSyCtaVbVYJrHPdbkj_gpxQWktZ-_5sJRyVk'})
    resonseJSON = response.json()

    if resonseJSON['status'] == 'OK':
        someResult = resonseJSON['results'][0]
        return {'lat':someResult['geometry']['location']['lat'],
                'lng':someResult['geometry']['location']['lng'],
                'formatted_address':someResult['formatted_address']}
    else:
        return None
