#!/usr/bin/env python

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import print_function

import requests


from urlparse import urlparse
import urllib2
from urllib import urlencode

try:
    import json
except ImportError:
    # Older versions of Python (i.e. 2.4) require simplejson instead of json
    import simplejson as json


if __name__ == '__main__':
    """
    Writes the API key to api_key.txt file. It will create the file if it doesn't exist.
    This function is intended to be called from the Python command line using: python alchemyapi YOUR_API_KEY
    If you don't have an API key yet, register for one at: http://www.alchemyapi.com/api/register.html

    INPUT:
    argv[1] -> Your API key from AlchemyAPI. Should be 40 hex characters

    OUTPUT:
    none
    """


    import sys
    if len(sys.argv) == 2 and sys.argv[1]:
        if len(sys.argv[1]) == 40:
            # write the key to the file
            f = open('api_key.txt', 'w')
            f.write(sys.argv[1])
            f.close()
            print('Key: ' + sys.argv[1] + ' was written to api_key.txt')
            print(
                'You are now ready to start using AlchemyAPI. For an example, run: python example.py')
        else:
            print(
                'The key appears to invalid. Please make sure to use the 40 character key assigned by AlchemyAPI')


class AlchemyAPI:
    # Setup the endpoints
    ENDPOINTS = {}
    ENDPOINTS['sentiment'] = {}
    ENDPOINTS['sentiment']['url'] = '/url/URLGetTextSentiment'
    ENDPOINTS['sentiment']['text'] = '/text/TextGetTextSentiment'
    ENDPOINTS['sentiment']['html'] = '/html/HTMLGetTextSentiment'
    ENDPOINTS['sentiment_targeted'] = {}
    ENDPOINTS['sentiment_targeted']['url'] = '/url/URLGetTargetedSentiment'
    ENDPOINTS['sentiment_targeted']['text'] = '/text/TextGetTargetedSentiment'
    ENDPOINTS['sentiment_targeted']['html'] = '/html/HTMLGetTargetedSentiment'
    ENDPOINTS['author'] = {}
    ENDPOINTS['author']['url'] = '/url/URLGetAuthor'
    ENDPOINTS['author']['html'] = '/html/HTMLGetAuthor'
    ENDPOINTS['keywords'] = {}
    ENDPOINTS['keywords']['url'] = '/url/URLGetRankedKeywords'
    ENDPOINTS['keywords']['text'] = '/text/TextGetRankedKeywords'
    ENDPOINTS['keywords']['html'] = '/html/HTMLGetRankedKeywords'
    ENDPOINTS['concepts'] = {}
    ENDPOINTS['concepts']['url'] = '/url/URLGetRankedConcepts'
    ENDPOINTS['concepts']['text'] = '/text/TextGetRankedConcepts'
    ENDPOINTS['concepts']['html'] = '/html/HTMLGetRankedConcepts'
    ENDPOINTS['entities'] = {}
    ENDPOINTS['entities']['url'] = '/url/URLGetRankedNamedEntities'
    ENDPOINTS['entities']['text'] = '/text/TextGetRankedNamedEntities'
    ENDPOINTS['entities']['html'] = '/html/HTMLGetRankedNamedEntities'
    ENDPOINTS['category'] = {}
    ENDPOINTS['category']['url'] = '/url/URLGetCategory'
    ENDPOINTS['category']['text'] = '/text/TextGetCategory'
    ENDPOINTS['category']['html'] = '/html/HTMLGetCategory'
    ENDPOINTS['relations'] = {}
    ENDPOINTS['relations']['url'] = '/url/URLGetRelations'
    ENDPOINTS['relations']['text'] = '/text/TextGetRelations'
    ENDPOINTS['relations']['html'] = '/html/HTMLGetRelations'
    ENDPOINTS['language'] = {}
    ENDPOINTS['language']['url'] = '/url/URLGetLanguage'
    ENDPOINTS['language']['text'] = '/text/TextGetLanguage'
    ENDPOINTS['language']['html'] = '/html/HTMLGetLanguage'
    ENDPOINTS['text'] = {}
    ENDPOINTS['text']['url'] = '/url/URLGetText'
    ENDPOINTS['text']['html'] = '/html/HTMLGetText'
    ENDPOINTS['text_raw'] = {}
    ENDPOINTS['text_raw']['url'] = '/url/URLGetRawText'
    ENDPOINTS['text_raw']['html'] = '/html/HTMLGetRawText'
    ENDPOINTS['title'] = {}
    ENDPOINTS['title']['url'] = '/url/URLGetTitle'
    ENDPOINTS['title']['html'] = '/html/HTMLGetTitle'
    ENDPOINTS['feeds'] = {}
    ENDPOINTS['feeds']['url'] = '/url/URLGetFeedLinks'
    ENDPOINTS['feeds']['html'] = '/html/HTMLGetFeedLinks'
    ENDPOINTS['microformats'] = {}
    ENDPOINTS['microformats']['url'] = '/url/URLGetMicroformatData'
    ENDPOINTS['microformats']['html'] = '/html/HTMLGetMicroformatData'
    ENDPOINTS['combined'] = {}
    ENDPOINTS['combined']['url'] = '/url/URLGetCombinedData'
    ENDPOINTS['combined']['text'] = '/text/TextGetCombinedData'
    ENDPOINTS['image'] = {}
    ENDPOINTS['image']['url'] = '/url/URLGetImage'
    ENDPOINTS['imagetagging'] = {}
    ENDPOINTS['imagetagging']['url'] = '/url/URLGetRankedImageKeywords'
    ENDPOINTS['imagetagging']['image'] = '/image/ImageGetRankedImageKeywords'
    ENDPOINTS['taxonomy'] = {}
    ENDPOINTS['taxonomy']['url'] = '/url/URLGetRankedTaxonomy'
    ENDPOINTS['taxonomy']['html'] = '/html/HTMLGetRankedTaxonomy'
    ENDPOINTS['taxonomy']['text'] = '/text/TextGetRankedTaxonomy'

    # The base URL for all endpoints
    BASE_URL = 'http://access.alchemyapi.com/calls'

    s = requests.Session()

    def __init__(self, use = 0):
        """
        Initializes the SDK so it can send requests to AlchemyAPI for analysis.
        It loads the API key from api_key.txt and configures the endpoints.
        """
        proxies = ['210.101.131.227:8080', '94.59.244.37:8118', '123.58.129.48:80',
        '119.6.144.74:82', '120.198.243.115:95', '114.249.36.220:8118',
        '124.88.67.13:80', '124.88.67.6:81', '120.131.128.213:80',
        '124.88.67.33:843', '211.144.81.66:18001', '210.101.131.227:8080',
        '111.161.126.100:80','115.239.210.199:80','221.5.69.51:80']
        apikeys = ['07ea6895c88e1c2797e9d0aa123cb66be86b4263',
        'c5f7096984ed1f9e7cb188ae3d47b23149986881',
        '63026da450ab17cac45b5d7edc959e27d80e4144',
        '613ff3c4201c8e2555616a39f48374bc1c5b9baa',
        '848e305062d1aaa5ced7b1de8ab217cfffe6b04e',
        '3027eb6c9c928aba2e56caee34494ca0f1061b72',
        'c44d4c75fc8aea9fa331884386ba5cd5b1625c92',
        'f4a4c28ca4877b99a63860a2115925ea8c345b9d',
        'dda49b90039d1388814241dfaa136d8cf3cfdea4',
        'da85c31da0a47e8cdfdfaa8ed528f04ebbbca6a1',
        'ef2ca19a69dc0e3c3f4478f67114528b444a1ce3',
        '115bbb0fd7b4cb50f7d696392b599aca820f41f4',
        '3e62447bb979222c7a747949ef056ca13d0d5eed',
        '624f83980b1850bc0ab8589daf3f8048e284b0f2',
        'ac98aac5461b5aef5c8d012a4d817f366b0e7dc8']

        proxy  = urllib2.ProxyHandler({'https': proxies[use]})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        self.apikey = apikeys[use]

    def entities(self, flavor, data, options={}):
        """
        Extracts the entities for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/entity-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/entity-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
        linkedData -> include linked data on disambiguated entities. 0: disabled, 1: enabled (default)
        coreference -> resolve coreferences (i.e. the pronouns that correspond to named entities). 0: disabled, 1: enabled (default)
        quotations -> extract quotations by entities. 0: disabled (default), 1: enabled.
        sentiment -> analyze sentiment for each entity. 0: disabled (default), 1: enabled. Requires 1 additional API transction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled
        maxRetrieve -> the maximum number of entities to retrieve (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['entities']:
            return {'status': 'ERROR', 'statusInfo': 'entity extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['entities'][flavor], {}, options)

    def keywords(self, flavor, data, options={}):
        """
        Extracts the keywords from text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/keyword-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/keyword-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        keywordExtractMode -> normal (default), strict
        sentiment -> analyze sentiment for each keyword. 0: disabled (default), 1: enabled. Requires 1 additional API transaction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the max number of keywords returned (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['keywords']:
            return {'status': 'ERROR', 'statusInfo': 'keyword extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['keywords'][flavor], {}, options)

    def concepts(self, flavor, data, options={}):
        """
        Tags the concepts for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/concept-tagging/
        For the docs, please refer to: http://www.alchemyapi.com/api/concept-tagging/

        Available Options:
        maxRetrieve -> the maximum number of concepts to retrieve (default: 8)
        linkedData -> include linked data, 0: disabled, 1: enabled (default)
        showSourceText -> 0:disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['concepts']:
            return {'status': 'ERROR', 'statusInfo': 'concept tagging for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['concepts'][flavor], {}, options)

    def sentiment(self, flavor, data, options={}):
        """
        Calculates the sentiment for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/sentiment-analysis/
        For the docs, please refer to: http://www.alchemyapi.com/api/sentiment-analysis/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        showSourceText -> 0: disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['sentiment']:
            return {'status': 'ERROR', 'statusInfo': 'sentiment analysis for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['sentiment'][flavor], {}, options)

    def sentiment_targeted(self, flavor, data, target, options={}):
        """
        Calculates the targeted sentiment for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/sentiment-analysis/
        For the docs, please refer to: http://www.alchemyapi.com/api/sentiment-analysis/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        target -> the word or phrase to run sentiment analysis on.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        showSourceText	-> 0: disabled, 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure the target is valid
        if target is None or target == '':
            return {'status': 'ERROR', 'statusInfo': 'targeted sentiment requires a non-null target'}

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['sentiment_targeted']:
            return {'status': 'ERROR', 'statusInfo': 'targeted sentiment analysis for ' + flavor + ' not available'}

        # add the URL encoded data and target to the options and analyze
        options[flavor] = data
        options['target'] = target
        return self.__analyze(AlchemyAPI.ENDPOINTS['sentiment_targeted'][flavor], {}, options)

    def text(self, flavor, data, options={}):
        """
        Extracts the cleaned text (removes ads, navigation, etc.) for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        useMetadata -> utilize meta description data, 0: disabled, 1: enabled (default)
        extractLinks -> include links, 0: disabled (default), 1: enabled.

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['text']:
            return {'status': 'ERROR', 'statusInfo': 'clean text extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['text'][flavor], options)

    def text_raw(self, flavor, data, options={}):
        """
        Extracts the raw text (includes ads, navigation, etc.) for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['text_raw']:
            return {'status': 'ERROR', 'statusInfo': 'raw text extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['text_raw'][flavor], {}, options)

    def author(self, flavor, data, options={}):
        """
        Extracts the author from a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/author-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/author-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Availble Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['author']:
            return {'status': 'ERROR', 'statusInfo': 'author extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['author'][flavor], {}, options)

    def language(self, flavor, data, options={}):
        """
        Detects the language for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/api/language-detection/
        For the docs, please refer to: http://www.alchemyapi.com/products/features/language-detection/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['language']:
            return {'status': 'ERROR', 'statusInfo': 'language detection for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['language'][flavor], {}, options)

    def title(self, flavor, data, options={}):
        """
        Extracts the title for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        useMetadata -> utilize title info embedded in meta data, 0: disabled, 1: enabled (default)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['title']:
            return {'status': 'ERROR', 'statusInfo': 'title extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['title'][flavor], {}, options)

    def relations(self, flavor, data, options={}):
        """
        Extracts the relations for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/relation-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/relation-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        sentiment -> 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
        keywords -> extract keywords from the subject and object. 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
        entities -> extract entities from the subject and object. 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
        requireEntities -> only extract relations that have entities. 0: disabled (default), 1: enabled.
        sentimentExcludeEntities -> exclude full entity name in sentiment analysis. 0: disabled, 1: enabled (default)
        disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
        linkedData -> include linked data with disambiguated entities. 0: disabled, 1: enabled (default).
        coreference -> resolve entity coreferences. 0: disabled, 1: enabled (default)
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the maximum number of relations to extract (default: 50, max: 100)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['relations']:
            return {'status': 'ERROR', 'statusInfo': 'relation extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['relations'][flavor], {}, options)

    def category(self, flavor, data, options={}):
        """
        Categorizes the text for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-categorization/
        For the docs, please refer to: http://www.alchemyapi.com/api/text-categorization/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        showSourceText -> 0: disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['category']:
            return {'status': 'ERROR', 'statusInfo': 'text categorization for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data

        return self.__analyze(AlchemyAPI.ENDPOINTS['category'][flavor], {}, options)

    def feeds(self, flavor, data, options={}):
        """
        Detects the RSS/ATOM feeds for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/feed-detection/
        For the docs, please refer to: http://www.alchemyapi.com/api/feed-detection/

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['feeds']:
            return {'status': 'ERROR', 'statusInfo': 'feed detection for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['feeds'][flavor], {}, options)

    def microformats(self, flavor, data, options={}):
        """
        Parses the microformats for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/microformats-parsing/
        For the docs, please refer to: http://www.alchemyapi.com/api/microformats-parsing/

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['microformats']:
            return {'status': 'ERROR', 'statusInfo': 'microformat extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['microformats'][flavor], {}, options)

    def imageExtraction(self, flavor, data, options={}):
        """
        Extracts main image from a URL

        INPUT:
        flavor -> which version of the call (url only currently).
        data -> URL to analyze
        options -> various parameters that can be used to adjust how the API works,
        see below for more info on the available options.

        Available Options:
        extractMode ->
             trust-metadata  :  (less CPU intensive, less accurate)
             always-infer    :  (more CPU intensive, more accurate)
        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        if flavor not in AlchemyAPI.ENDPOINTS['image']:
            return {'status': 'ERROR', 'statusInfo': 'image extraction for ' + flavor + ' not available'}
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['image'][flavor], {}, options)

    def taxonomy(self, flavor, data, options={}):
        """
        Taxonomy classification operations.

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.


        Available Options:
        showSourceText  ->
            include the original 'source text' the taxonomy categories were extracted from within the API response
            Possible values:
                1 - enabled
                0 - disabled (default)

        sourceText ->
            where to obtain the text that will be processed by this API call.

            AlchemyAPI supports multiple modes of text extraction:
                web page cleaning (removes ads, navigation links, etc.), raw text extraction
                (processes all web page text, including ads / nav links), visual constraint queries, and XPath queries.

            Possible values:
                cleaned_or_raw  : cleaning enabled, fallback to raw when cleaning produces no text (default)
                cleaned         : operate on 'cleaned' web page text (web page cleaning enabled)
                raw             : operate on raw web page text (web page cleaning disabled)
                cquery          : operate on the results of a visual constraints query
                                  Note: The 'cquery' http argument must also be set to a valid visual constraints query.
                xpath           : operate on the results of an XPath query
                                  Note: The 'xpath' http argument must also be set to a valid XPath query.

        cquery ->
            a visual constraints query to apply to the web page.

        xpath ->
            an XPath query to apply to the web page.

        baseUrl ->
            rel-tag output base http url (must be uri-argument encoded)

        OUTPUT:
        The response, already converted from JSON to a Python object.

        """
        if flavor not in AlchemyAPI.ENDPOINTS['taxonomy']:
            return {'status': 'ERROR', 'statusInfo': 'taxonomy for ' + flavor + ' not available'}
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['taxonomy'][flavor], {}, options)

    def combined(self, flavor, data, options={}):
        """
        Combined call for page-image, entity, keyword, title, author, taxonomy,  concept.

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        extract ->
            Possible values: page-image, entity, keyword, title, author, taxonomy,  concept
            default        : entity, keyword, taxonomy,  concept

        disambiguate ->
            disambiguate detected entities
            Possible values:
                1 : enabled (default)
                0 : disabled

        linkedData ->
            include Linked Data content links with disambiguated entities
            Possible values :
                1 : enabled (default)
                0 : disabled

        coreference ->
            resolve he/she/etc coreferences into detected entities
            Possible values:
                1 : enabled (default)
                0 : disabled

        quotations ->
            enable quotations extraction
            Possible values:
                1 : enabled
                0 : disabled (default)

        sentiment ->
            enable entity-level sentiment analysis
            Possible values:
                1 : enabled
                0 : disabled (default)

        showSourceText ->
            include the original 'source text' the entities were extracted from within the API response
            Possible values:
                1 : enabled
                0 : disabled (default)

        maxRetrieve ->
            maximum number of named entities to extract
            default : 50

        baseUrl ->
            rel-tag output base http url


        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        if flavor not in AlchemyAPI.ENDPOINTS['combined']:
            return {'status': 'ERROR', 'statusInfo': 'combined for ' + flavor + ' not available'}
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['combined'][flavor], {}, options)

    def imageTagging(self, flavor, data, options={}):
        """

        INPUT:
        flavor -> which version of the call only url or image.
        data -> the data to analyze, either the the url or path to image.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
        """
        if flavor not in AlchemyAPI.ENDPOINTS['imagetagging']:
            return {'status': 'ERROR', 'statusInfo': 'imagetagging for ' + flavor + ' not available'}
        elif 'image' == flavor:
            image = open(data, 'rb').read()
            options['imagePostMode'] = 'raw'
            return self.__analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], options, image)

        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], {}, options)

    def __analyze(self, endpoint, params, post_data=bytearray()):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface.
        It makes the call, then converts the returned JSON string into a Python object.

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Add the API Key and set the output mode to JSON
        params['apikey'] = self.apikey
        params['outputMode'] = 'json'
        # Insert the base url

        post_url = ""
        try:
            post_url = AlchemyAPI.BASE_URL + endpoint + \
                '?' + urlencode(params).encode('utf-8')
        except TypeError:
            post_url = AlchemyAPI.BASE_URL + endpoint + '?' + urlencode(params)

        results = ""
        try:
            results = self.s.post(url=post_url, data=post_data)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}
