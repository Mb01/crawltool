#!/usr/bin/python2.7


#   follows links, stay in domain to create huge blobs of html
#   

#   try grep -o -P "http[^<>]*?\.jpg" file* > jpgs to get jpgs out of a file

# else try this

#   ./htmlGrab.py http://example.com | grep -o -P "http[^<>]*?\.jpg" >> jpgs
print 'try: htmlGrab.py -s http://example.com | grep -o -P "http[^<>]*?\.jpg" >> jpgs'
print 'to get lots of images or whatever' + '\n'


from argparse import ArgumentParser
import sys
from urllib2 import urlopen, URLError, HTTPError
from urlparse import urlparse
import time
import random
from bs4 import BeautifulSoup as bs
import re
import os
import httplib


DOMAIN = ""


#    FUNCTIONS

def crawl( seed ):
    LINKS = [seed]
    VISITED = []
    #FILE = open(args.logfile, "a")
    while LINKS:
        link = random.choice( LINKS )
        LINKS.remove( link )
        sys.stderr.write("links left: " + str( len(link) ) + '\n')
        if link.find('@') != -1:
            continue
        page = False
        sys.stderr.write("trying %s" % link + '\n')
        try:
            page = urlopen( link ).read()
        except (IOError, URLError, HTTPError, ValueError, AttributeError, httplib.IncompleteRead) as e:
            sys.stderr.write("Couldn't read %s because of %s" % ((link),str(e))+ '\n')
        if not page:
            sys.stderr.write("Somehow we didn't get a response"+ '\n')
            continue
        VISITED.append( link )
        print page
        #FILE.write(page)
                
        soup = bs(page)
        for a in soup.find_all('a'):
            href = a.get('href')
            try:
                href = href.encode('utf-8')
                if href not in VISITED and str(href).find('http') == 0 and not re.match( r'.*jpg',  href ):
                    if str( urlparse(href).netloc ) == DOMAIN:                                            
                        LINKS.append(href)
                if str(href).find('/') == 0 and href not in VISITED:
                    LINKS.append( DOMAIN + href )
            except UnicodeError as e:
                sys.stderr.write(str(e)+ '\n')


#       PARSE ARGS

parser = ArgumentParser()

parser.add_argument("seed", help="a url to start from")
#parser.add_argument("-l", "--logfile", help="where to store links" )

args = parser.parse_args()

while not args.seed: args.seed = raw_input("Seed url: ")
#while not args.logfile: args.logfile = raw_input("File to append results: ")



DOMAIN = str( urlparse(args.seed).netloc )






crawl( args.seed )

