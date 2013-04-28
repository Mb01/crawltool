#!/usr/bin/python2.7


import os
import argparse


"Use a redirection ( > ) to save output"



"try:"
' ls | sed -r "s|%|/|g" > out'
"to change % to / or whatever you need"



parser = argparse.ArgumentParser()

parser.add_argument('linklist')
parser.add_argument('inventory')

args = parser.parse_args()

linklist = open(args.linklist, "r").read().split('\n')
inventory = open(args.inventory, "r").read().split('\n')

NEWlinklist = []

for x in linklist:
    if x not in inventory:
        print x
