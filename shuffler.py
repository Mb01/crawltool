#!/usr/bin/python2.7

import argparse
import random

parser = argparse.ArgumentParser()

parser.add_argument('file', help ='a file with lines to shuffle')

args = parser.parse_args()

load = open(args.file).read().split('\n')

random.shuffle(load)

write = open(args.file, "w")

for x in load:
    write.write(x + '\n')
write.close()
