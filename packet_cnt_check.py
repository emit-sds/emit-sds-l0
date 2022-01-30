#!/usr/bin/env python

import argparse

import emit.data_products as dp

parser = argparse.ArgumentParser()
parser.add_argument('infile')
args = parser.parse_args()

in_file = open(args.infile, 'rb')

cnt = 0
while True:
    try:
        dp.CCSDSPacket(in_file)
        cnt += 1
    except EOFError:
        break

print(cnt)
