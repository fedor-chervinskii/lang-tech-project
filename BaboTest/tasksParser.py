#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymorphy2
from collections import OrderedDict

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
    tokenizedTask = frozenset(task['taskInfo']['searchKeywords'])
    tokenizedTweet = frozenset(tweet.text.split(' '))
    print tokenizedTask.intersection(tokenizedTweet)
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
