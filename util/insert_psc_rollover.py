#!/usr/bin/env python

import argparse

import emit.data_products as dp

HOSC_HEADER_SIZE = 28
MAX_PSC = 790


def main():

    parser = argparse.ArgumentParser(
        description="Artificially insert a PSC rollover in a HOSC stream for testing purposes"
    )
    parser.add_argument('input_file')
    args = parser.parse_args()

    in_file = open(args.input_file, 'rb')
    outfile = open(args.input_file.replace(".bin", "_rollover.bin"), "wb")

    cnt = 0
    while True:
        try:
            # Read past HOSC header
            hosc_hdr = in_file.read(HOSC_HEADER_SIZE)

            # Read in packet and copy header to update PSCs
            pkt = dp.CCSDSPacket(in_file)
            hdr = bytearray(pkt.hdr_data)

            print(f"PSC before: {pkt.pkt_seq_cnt}")
            pkt.pkt_seq_cnt = pkt.pkt_seq_cnt % MAX_PSC
            print(f"PSC after: {pkt.pkt_seq_cnt}")

            # Update PSC bytes in header
            psc_bytes = pkt.pkt_seq_cnt.to_bytes(2, byteorder="big", signed=False)
            print("psc: " + str([bin(psc_bytes[i])[2:].zfill(8) for i in range(2)]))
            # Reset 14 bits of PSC to 0
            hdr[2] = hdr[2] & 0xC0
            hdr[3] = 0x00
            # Add new PSC (preserving the leftmost 2 bits)
            hdr[2] = hdr[2] | psc_bytes[0]
            hdr[3] = hdr[3] | psc_bytes[1]

            # Write out file
            outfile.write(hosc_hdr)
            outfile.write(hdr)
            outfile.write(pkt.body)
            cnt += 1
        except EOFError:
            break

    print(f"Count: {cnt}")


if __name__ == "__main__":
    main()
