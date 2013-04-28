#!/usr/bin/python2.7
from argparse import ArgumentParser
import sys
from urllib2 import urlopen, URLError, HTTPError
from urlparse import urlparse
import time
import random
from bs4 import BeautifulSoup as bs
import re
import os

SAVEPATH = ""

#    FUNCTIONS

def savePic( url ):
    p = urlparse( url )
    filestring = str( p.netloc + p.path ).replace('/','%' )
    if os.path.isfile( SAVEPATH + filestring ):
        return
    picFile = open(SAVEPATH + filestring , "w" )
    pic = urlopen( url ).read()
    picFile.write( pic )
    picFile.close()

def crawl( seed ):
    LINKS = [seed]
    VISITED = []
    FILE = open(args.logfile, "a")
    while LINKS:
        link = random.choice( LINKS )
        LINKS.remove( link )
        if link.find('@') != -1:
            continue
        print "trying %s" % link
        try:
            page = urlopen( link ).read()
        except (IOError, URLError, HTTPError, ValueError, AttributeError) as e:
            print "Couldn't read %s because of %s" % (link, e)
        VISITED.append( link )
        soup = bs(page)
        for a in soup.find_all('a'):
            href = a.get('href')
            try:
                if href not in VISITED and str(href).find('http') == 0 and not re.match( r'.*jpg',  href ):
                        LINKS.append(href)
                        FILE.write(str(href) + '\n')
            except UnicodeError as e:
                print e
        
def getPics( url ):
    page = urlopen( url ).read()
    if page:
        soup = bs(page)
        pics = []
        for x in soup.find_all('a'):
            href = str( x.get('href') )
            if re.match( r'.*jpg',  href ):
                pics.append( href )
    return pics


#       PARSE ARGS

parser = ArgumentParser()

parser.add_argument("-s", "--seed", help="a url to start from")
parser.add_argument("-l", "--logfile", help="where to store links" )
parser.add_argument("-m", "--mode",
                    choices=["savepics","links","piclinks"],
                    help="what mode")
parser.add_argument("-lf", "--linksfile", help="where to get links from")
parser.add_argument("--sleeptime", help="seconds between pictures", default=2, type=int)
parser.add_argument("-sp", "--savepath", help="where to save picture output")

args = parser.parse_args()


#       SETUP SAVE PATH for multi-file ouput... for single in out just include path in the argument
#                                               or just cd to that directory
if args.savepath:
    SAVEPATH = args.savepath + os.sep    
else:
    SAVEPATH = "pics/"
if not os.path.exists( SAVEPATH ):
    os.makedirs( SAVEPATH )


#       DEMAND A MODE
while not args.mode: args.mode = raw_input("Mode (savepics, links, piclinks): ")


if args.mode == "savepics":
#                ^^^^^^^^
    if not args.linksfile: args.linksfile = "pic.links"
    
    fil = open(args.linksfile, "r")
    links = fil.read().split('\n')

    for x in links:
        print "trying: ", x
        try:
            savePic( x )
        except (IOError, URLError, HTTPError, ValueError, AttributeError) as e:
            print e
            
        time.sleep( args.sleeptime )
    sys.exit()

if args.mode == "links":
#                ^^^^^
    if not args.logfile: args.logfile = "page.links"
    
    if not args.seed: args.seed = raw_input("URL to start from: ")
    if not args.seed: sys.exit()
    
    crawl( args.seed )

if args.mode == "piclinks":
#                ^^^^^^^^
    if not args.logfile: args.logfile = "pic.links"
    if not args.linksfile: args.linksfile = "page.links"
    
    links = open(args.linksfile, "r").read().split('\n')
    log = open(args.logfile, "a")
    
    for x in links:
        print "trying page: " , x
        pics = []
        try:
            pics = getPics( x )
        except (IOError, URLError, HTTPError, ValueError, AttributeError) as e:
            print e
        if pics:
            for y in pics:
                log.write( str(y) + '\n' )

