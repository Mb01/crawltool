#!/usr/bin/python2.7

import argparse
from urllib2 import *
from urlparse import urlparse
import os
import httplib

#   take input

SAVEPATH = "pics/"

parser = argparse.ArgumentParser()

parser.add_argument('file', help ='a file with newline delimited urls to retrieve and save')

args = parser.parse_args()

toLoad = open(args.file).read().split('\n')


def savePic( url ):
    p = urlparse( url )
    filestring = str( p.netloc + p.path ).replace('/','%' )
    if os.path.isfile( SAVEPATH + filestring ):
        return
    picFile = open(SAVEPATH + filestring , "w" )
    pic = urlopen( url ).read()
    picFile.write( pic )
    picFile.close()

for x in toLoad:
    try:
        savePic( x )
    except (IOError, URLError, UnicodeError, HTTPError, ValueError, AttributeError,httplib.IncompleteRead) as e:
        print e
