#!/usr/bin/python2.7

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("file", help="a file to make each line unique")
args = parser.parse_args()

fil = open(args.file, "r")
contents = fil.read().split('\n')

fil.close()


#
#   HERE IS WHERE THE "MAGIC" HAPPENS
#

contents = list( set( contents ) )

#
#
#

fil = open(args.file, "w")

for x in contents:
	fil.write( x + '\n' )

fil.close()

