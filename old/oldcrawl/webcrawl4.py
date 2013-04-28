#short version web crawler
import urllib2
from bs4 import BeautifulSoup as bs
import argparse
import random
parser = argparse.ArgumentParser()
parser.add_argument("seed", help="a url to start from")
args = parser.parse_args()
LINKS = []
VISITED = []

def crawl( seed ):
    global LINKS
    global VISITED
    LINKS.append( seed )
    file = open('links.txt', 'a')
    
    while LINKS:
        link = random.choice( LINKS )
        print "trying %s" % link
        
        try:
            page = urllib2.urlopen( link ).read()
        except (IOError, urllib2.URLError, urllib2.HTTPError, ValueError, AttributeError) as e:
            print "Couldn't read %s because of %s" % (link, e)
        
        soup = bs(page)
        for a in soup.find_all('a'):
            href = a.get('href')
            if href not in VISITED and str(href).find('http') == 0:
                LINKS.append(href)        
        file.write(str(link) + '\n')
    
    file.close()
crawl(args.seed)
