__author__ = 'denisantyukhov'

from BeautifulSoup import *
import urllib2
import json

url = "http://proxylist.hidemyass.com/search-1346407#listable"
soup = BeautifulSoup(urllib2.urlopen(url).read())
tables = soup.findAll('table')
for table in tables:
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        ip = cols.findALL
print cols[]









