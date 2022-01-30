#!/usr/bin/env python

import argparse

import emit.data_products as dp

HOSC_HEADER_SIZE = 28
HOSC_HEADER = bytes(HOSC_HEADER_SIZE)


def main():

    parser = argparse.ArgumentParser(
        description="Given a HOSC stream, reverse the order of the packets"
    )
    parser.add_argument('input_file')
    args = parser.parse_args()

    in_file = open(args.input_file, 'rb')

    cnt = 0
    reversed_packets = []
    while True:
        try:
            hosc_hdr = in_file.read(HOSC_HEADER_SIZE)
            pkt = dp.CCSDSPacket(in_file)
            reversed_packets.insert(0, pkt)
            cnt += 1
        except EOFError:
            break

    print(f"Count: {cnt}")

    with open(args.input_file.replace(".bin", "_reversed.bin"), "wb") as outfile:
        for i in range(len(reversed_packets)):
            pkt = reversed_packets[i]
            print(f"PSC: {pkt.pkt_seq_cnt}")
            outfile.write(HOSC_HEADER)
            outfile.write(pkt.hdr_data)
            outfile.write(pkt.body)


if __name__ == "__main__":
    main()
