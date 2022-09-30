#!/usr/bin/env python

import argparse

from emit_sds_l1a.ccsds_packet import ScienceDataPacket

HOSC_HEADER_LEN = 28

parser = argparse.ArgumentParser()
parser.add_argument("infile")
args = parser.parse_args()

# in_file = open(args.infile, "rb")
prev_pkt = None
count = 0

with open(args.infile, "rb") as f:
    while True:
        try:
            # Read hosc header
            hosc_header = f.read(HOSC_HEADER_LEN)
            # Read a packet
            pkt = ScienceDataPacket(stream=f)
            if prev_pkt is not None and (prev_pkt.pkt_seq_cnt + 1) % 16384 != pkt.pkt_seq_cnt:
                print(f"Out of order - prev_psc is {prev_pkt.pkt_seq_cnt}, current psc is {pkt.pkt_seq_cnt}")
                print(f"Previous: {prev_pkt}")
                print(f"Current: {pkt}")
            prev_pkt = pkt
            count += 1
        except EOFError:
            break

print(f"Total packets: {count}")

