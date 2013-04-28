#short version web crawler
from bs4 import BeautifulSoup as b
import argparse, random, urllib2
V,F,P = ([],open('l.txt', 'a'),argparse.ArgumentParser())
P.add_argument("s")
a = P.parse_args()
L = [a.s]
while L:
    l = random.choice(L)
    try:
        s = b(urllib2.urlopen(l).read())
    except (IOError, urllib2.URLError, urllib2.HTTPError, ValueError, AttributeError) as e:
        print e
    for a in s.find_all('a'):
        h = a.get('href')
        if h not in V and str(h).find('http') == 0:
            L.append(h)
    F.write(str(l)+'\n')
F.close()
