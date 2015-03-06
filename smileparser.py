__author__ = 'denisantyukhov'
from BeautifulSoup import *
import urllib2
import json
dct = {}
url = "http://apps.timwhitlock.info/emoji/tables/unicode"
soup = BeautifulSoup(urllib2.urlopen(url).read())
tables = soup.findAll(attrs={'class': 'table table-bordered table-striped'})
for table in tables:
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if (len(cols)>9):
            dct[cols[9].renderContents().lower()] = cols[0].span.text

with open('emoji_database','w') as json_file:
                json.dump(dct, json_file)





