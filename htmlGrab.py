#!/usr/bin/python2.7


#   follows links to create huge blobs of html
#   

#   try grep -o -P "http[^<>]*?\.jpg" file* > jpgs to get jpgs out of the file


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

SAVEPATH = ""

#    FUNCTIONS

def crawl( seed ):
    LINKS = [seed]
    VISITED = []
    #FILE = open(args.logfile, "a")
    while LINKS:
        link = random.choice( LINKS )
        LINKS.remove( link )
        if link.find('@') != -1:
            continue
        page = False
        print "trying %s" % link
        try:
            page = urlopen( link ).read()
        except (IOError, URLError, HTTPError, ValueError, AttributeError, httplib.IncompleteRead) as e:
            print "Couldn't read %s because of %s" % (link, e)
        if not page:
            print "Somehow we didn't get a response"
            continue
        VISITED.append( link )
        print page        
        #FILE.write(page)
                
        soup = bs(page)
        for a in soup.find_all('a'):
            href = a.get('href')
            try:
                if href not in VISITED and str(href).find('http') == 0 and not re.match( r'.*jpg',  href ):
                        LINKS.append(href)
            except UnicodeError as e:
                print e


#       PARSE ARGS

parser = ArgumentParser()

parser.add_argument("seed", help="a url to start from")
#parser.add_argument("-l", "--logfile", help="where to store links" )

args = parser.parse_args()

while not args.seed: args.seed = raw_input("Seed url: ")
#while not args.logfile: args.logfile = raw_input("File to append results: ")

crawl( args.seed )


