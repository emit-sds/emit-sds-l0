#!/usr/bin/env python

import argparse

from emit_sds_l1a.ccsds_packet import ScienceDataPacket

HOSC_HEADER_LEN = 28

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("coarse_time", type=int)
parser.add_argument("fine_time", type=int)
parser.add_argument("psc", type=int)
args = parser.parse_args()

print(f"Args are coarse={args.coarse_time}, fine={args.fine_time}, and psc={args.psc}")

prev_pkt = None
count = 0

with open(args.infile, "rb") as f:
    while True:
        try:
            # Read hosc header
            hosc_header = f.read(HOSC_HEADER_LEN)
            # Read a packet
            pkt = ScienceDataPacket(stream=f)

            if pkt.coarse_time == args.coarse_time and pkt.fine_time == args.fine_time and pkt.pkt_seq_cnt == args.psc:
                print(f"Found packet with coarse={args.coarse_time}, fine={args.fine_time}, and psc={args.psc}")
                
            if pkt.coarse_time == args.coarse_time and pkt.pkt_seq_cnt == args.psc:
                print(f"Found packet with coarse={args.coarse_time}, and psc={args.psc}")
                
            count += 1
        except EOFError:
            break

print(f"Total packets: {count}")

