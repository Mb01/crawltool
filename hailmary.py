#!/usr/bin/python2.7

#   this version does everything in one go



from argparse import ArgumentParser
import sys
from urllib2 import urlopen, URLError, HTTPError
from urlparse import urlparse
import time
import random
from bs4 import BeautifulSoup as bs
import re
import os
import atexit

SAVEPATH = ""


def savePic( url ):
    p = urlparse( url )
    filestring = str( p.netloc + p.path ).replace('/','%' )
    if os.path.isfile( SAVEPATH + filestring ):
        return
    picFile = open(SAVEPATH + filestring , "w" )
    pic = urlopen( url ).read()
    picFile.write( pic )
    picFile.close()

def getSoup( link ):
    print "trying %s" % link
    page = ""
    try:
        page = urlopen( link ).read()
    except (IOError, URLError, HTTPError, ValueError, AttributeError) as e:
        print "Couldn't read %s because of %s" % (link, e)
    return bs(page)

VISITED = []
LINKS = []

def crawl( seed ):
    global LINKS    
    LINKS = [seed]
    global VISITED
    FILE = open(args.logfile, "a")
    FILE.write("\n\n\n::BEGINSESSION::\n\n\n")
    FILE.write(time.ctime(time.time()))
    while LINKS:
        link = random.choice( LINKS )
        LINKS.remove( link )
        if link.find('@') != -1:#   leave email addresses alone
            continue
        FILE.write(str( link ) + '\n')
        soup = getSoup( link )
        VISITED.append( link )
        try:
            targets = soup.find_all('a')
            for a in targets:
                href = str( a.get('href') )
                try:
                    #   add all viable links found to LINKS
                    if href not in VISITED and str(href).find('http') == 0 and not re.match( r'.*jpg',  href ):
                        LINKS.append(href)
                    #   download viable jpg links
                    pics = re.match( r'.*jpg',  href )
                    if pics:
                        savePic( href )
                        FILE.write( "\t" + str(href) + "\n" )
                except (UnicodeEncodeError, UnicodeError, IOError, URLError, HTTPError, ValueError, AttributeError) as e:
                    print e
        except (UnicodeEncodeError) as e:
            print e

@atexit.register
def endlog():
    FILE = open(args.logfile, "a")
    FILE.write("\n\n\n::ENDSESSION::\n\n\n")
    FILE.write("\n\n::UNVISITED::\n")
    for x in LINKS:
        FILE.write( str( x ) )
    FILE.write("\n\n\n::ENDRECORD::\n\n\n")

    


#       PARSE ARGS

parser = ArgumentParser()

parser.add_argument("-s", "--seed", help="a url to start from")
parser.add_argument("--sleeptime", help="seconds between pictures", default=2, type=int)
parser.add_argument("-sp", "--savepath", help="where to save picture output")
parser.add_argument("-l", "--logfile", help="where to store links" )
args = parser.parse_args()


#       SETUP SAVE PATH for multi-file ouput... for single in out just include path in the argument
#                                               or just cd to that directory
if args.savepath:
    SAVEPATH = args.savepath + os.sep    
else:
    SAVEPATH = "pics/"
if not os.path.exists( SAVEPATH ):
    os.makedirs( SAVEPATH )

#   DEMAND A SEED PAGE

while not args.seed: args.seed = raw_input("URL to start from: ")

#   ENSURE A LOGFILE
if not args.logfile: args.logfile = SAVEPATH + "out.log"

crawl( args.seed )





