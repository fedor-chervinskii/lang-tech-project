__author__ = 'denisantyukhov'
from urllib.request import urlopen
from BeautifulSoup import *
import urllib2
import json

import urllib2

proxy  = urllib2.ProxyHandler({'https': '210.101.131.227:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

my_ip = urllib2.urlopen('http://whatthehellismyip.com/?ipraw').read()
print my_ip


dct = {}
url = "http://cool-smileys.com/text-emoticons"
soup = BeautifulSoup(urllib2.urlopen(url).read())
tables = soup.findAll('table')
for table in tables:
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if len(cols):
            if cols[0].find('a').getText() != 'Cheshire cat' and cols[0].find('a').getText() != 'dunce':
                print cols[0].find('a').getText()
                dct[str(cols[2].find('input')['value'])] = cols[0].find('a').getText()

url = "http://cool-smileys.com/text-emoticons-part2"
soup = BeautifulSoup(urllib2.urlopen(url).read())
tables = soup.findAll('table')
for table in tables:
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if len(cols):
            if cols[0].find('a').getText() != 'Mickey Mouse' and cols[0].find('a').getText() != 'one eyebrow raised' and cols[0].find('a').getText() != 'One-Eyed Smile':
                print cols[0].find('a').getText()
                dct[str(cols[2].find('input')['value'])] = cols[0].find('a').getText()


with open('emoji_txt_db.json', 'wb') as fp:
    json.dump(dct, fp)







