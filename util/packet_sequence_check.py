#!/usr/bin/env python

import argparse

import emit.data_products as dp

HOSC_HEADER_LEN = 28

parser = argparse.ArgumentParser()
parser.add_argument("infile")
args = parser.parse_args()

in_file = open(args.infile, "rb")
prev_psc = 0
count = 0

with open(in_file, "rb") as f:
    while True:
        try:
            # Read hosc header
            hosc_header = f.read(HOSC_HEADER_LEN)
            # Read a packet
            pkt = dp.CCSDSPacket(stream=f)
            if (prev_psc + 1) % 16384 != pkt.pkt_seq_cnt and count > 0:
                print(f"Out of order - prev_psc is {prev_psc}, current psc is {pkt.pkt_seq_cnt}")
                print(pkt)
            count += 1
        except EOFError:
            break

print(f"Total packets: {count}")
