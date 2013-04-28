#short version web crawler
from bs4 import BeautifulSoup as bs
import argparse, random, urllib2
LINKS, VISITED, FILE, PARSER = ([],[], open('links.txt', 'a'), argparse.ArgumentParser())
PARSER.add_argument("seed", help="a url to start from")
args = PARSER.parse_args()
LINKS.append(args.seed)
while LINKS:
    link = random.choice(LINKS)
    print "trying %s" % link
    try:
        soup = bs(urllib2.urlopen(link).read())
    except (IOError, urllib2.URLError, urllib2.HTTPError, ValueError, AttributeError) as e:
        print "Couldn't read %s because of %s" % (link, e)
    for a in soup.find_all('a'):
        href = a.get('href')
        if href not in VISITED and str(href).find('http') == 0:
            LINKS.append(href)        
    FILE.write(str(link)+'\n')
FILE.close()

