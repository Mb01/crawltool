#short version web crawler with threading
import thread

import time

import urllib2
from bs4 import BeautifulSoup as bs
import argparse
import random

LINKS = []
VISITED = []

FILE = open('links3.txt', 'a')

FILE_LOCK = thread.allocate_lock()
LINKS_LOCK = thread.allocate_lock()
VISITED_LOCK = thread.allocate_lock()

parser = argparse.ArgumentParser()
parser.add_argument("seed", help="a url to start from")
args = parser.parse_args()

LINKS.append( args.seed )



def crawl():
    global LINKS
    global VISITED
    global FILE
    
    while LINKS:
        with LINKS_LOCK:
            link = random.choice( LINKS )
            LINKS.remove( link )
        print "trying %s" % link
        
        try:
            page = urllib2.urlopen( link ).read()
        except (IOError, urllib2.URLError, urllib2.HTTPError, ValueError, AttributeError) as e:
            print "Couldn't read %s because of %s" % (link, e)
        
        with VISITED_LOCK:
            VISITED.append( link )
            soup = bs(page)
            for a in soup.find_all('a'):
                href = a.get('href')
                try:
                    if href not in VISITED and str(href).find('http') == 0:
                        with LINKS_LOCK:
                            LINKS.append(href)
                except UnicodeError as e:
                    print e
        with FILE_LOCK:
            FILE.write(str(link) + '\n')


thread.start_new_thread(crawl, ())
time.sleep(50)
thread.start_new_thread(crawl, ())
time.sleep(50)
thread.start_new_thread(crawl, ())
time.sleep(200)
thread.start_new_thread(crawl, ())
