#downloads all the pics in a log
from urllib2 import *
import hashlib
import time

links = open("log.txt", "r").read().split('\n')

def savePic( url ):
    filestring = hashlib.md5(url).hexdigest()
    filestring = "z" + filestring[:10] + ".jpg"
    picFile = open( filestring , "wb" )
    pic = urlopen( url ).read()
    picFile.write( pic )
    picFile.close()

for x in links:
    savePic(x)
    time.sleep(2)