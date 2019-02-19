#!/usr/bin/python2.7

# Provided a list of urls (intended to be pointnig to images)
# this saves all the newline delimited urls in a file to files in a pic directory
# Please make a directory and suppy it via the commandline when prompted.

# To add flexibility and not perform unwanted overwrting, the program asks for a directory.
# Note, this program should be updated to take the directory as an argument

import argparse
from urllib2 import *
from urlparse import urlparse
import os
import httplib
import time

# parse command line 
parser = argparse.ArgumentParser()

parser.add_argument('file', help ='a file with newline delimited urls to retrieve and save')

args = parser.parse_args()

toLoad = open(args.file).read().split('\n')

SAVEPATH = raw_input('savepath?: ')

if SAVEPATH[-1] != '/':
    SAVEPATH += '/'
if not os.path.isdir(SAVEPATH):
    if os.path.exists(SAVEPATH):
        os.stderr.write('Error: Exists but is not a directory')
    else:
        os.mkdir(SAVEPATH)

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
