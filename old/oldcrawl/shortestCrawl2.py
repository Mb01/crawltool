#shorter version web crawler sacrificing all readability
from bs4 import BeautifulSoup as bs
import sys, random, urllib2
LINKS, VISITED, FILE = ([sys.argv[1]],[], open('links2.txt', 'a'))
while LINKS:
    link = random.choice(LINKS)
    try:
        for href in [x.get('href') for x in bs(urllib2.urlopen(link).read()).find_all('a')]:
            if href not in VISITED and str(href).find('http') == 0: LINKS.append(href)
    except (IOError, urllib2.URLError, urllib2.HTTPError, ValueError, AttributeError) as e:
        print "Couldn't read %s because of %s" % (link, e)
    FILE.write(str(link)+'\n')
FILE.close()
