from urllib2 import *
from bs4 import BeautifulSoup as bs
import urlparse as up
import re
import hashlib

LOGSTRING = ""

def getLinks():
    file = open("links.txt", "r")
    links = file.read().split('\n')
    file.close()
    return links

def savePic( url ):
    filestring = hashlib.md5(url)[:15] +".jpg"
    picFile = open( filestring , "wb" )
    pic = urlopen( url ).read()
    picFile.write( pic )
    picFile.close()
        
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


logfile = open("log.txt", "a")

links = getLinks()
    
while links:
    for x in links:
        print "trying page: " , x
        try:
            pics = getPics( x )
        except (IOError, URLError, HTTPError, ValueError, AttributeError) as e:
            print e
            continue
                
        for x in pics:
            try:
                print "trying picture: " , x
                savePic( x )
            except (IOError, URLError, HTTPError, ValueError, AttributeError, OSError, IOError) as e:
                print e
                

