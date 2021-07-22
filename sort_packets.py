#!/usr/bin/env python
 
import argparse
from collections import OrderedDict
from sortedcontainers import SortedDict
 
import emit.data_products as dp

HOSC_HEADER_SIZE = 28


def sort_pscs(psc_dict):
    sorted = OrderedDict()
    for k in sorted(psc_dict.keys()):
        sorted[k] = psc_dict[k]
    print(sorted)



def main():

    parser = argparse.ArgumentParser(
        description="Sort CCSDS packets into time-ordered and PSC-ordered series"
    )
    parser.add_argument('input_file')
    args = parser.parse_args()

    in_file = open(args.input_file, 'rb')

    cnt = 0
    pkts = SortedDict()
    while True:
        try:
            hosc_hdr = in_file.read(HOSC_HEADER_SIZE)
            pkt = dp.CCSDSPacket(in_file)
            print(pkt)
            course_time = int.from_bytes(pkt.body[:4], "big")
            fine_time = pkt.body[4]
            psc = pkt.pkt_seq_cnt
            print(f"<course={course_time} fine={fine_time} psc={psc}>")
            time_key = str(course_time).zfill(10) + str(fine_time).zfill(3)
            # print(f"time_key: {time_key}")
            if time_key in pkts:
                # print(psc)
                pkts[time_key][psc] = pkt
                # sort_pscs(pkts[time_key])
            else:
                pkts[time_key] = SortedDict()
                pkts[time_key][psc] = pkt

            cnt += 1
        except EOFError:
            break

    print(f"Count: {cnt}")

    # Iterate over pkts
    for time, pscs in pkts.items():
        for psc in pscs.keys():
            print(f"{time}: {psc}")


if __name__ == "__main__":
    main()