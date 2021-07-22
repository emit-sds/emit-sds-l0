#!/usr/bin/env python
 
import argparse
from sortedcontainers import SortedDict
 
import emit.data_products as dp

HOSC_HEADER_SIZE = 28
HOSC_HEADER = bytes(28)
MAX_PSC = 790


def sort_packets_by_psc(packets):
    # This function sorts packets in a given course_time + fine_time group where PSCs have rolled over
    # due to hitting the MAX_PSC limit.  This condition is met when the min and max PSCs in a particular
    # group differ by more than 256 (an arbitrary number, but so far, I haven't seen more than 8 PSCs
    # in a given group).
    for psc, pkt in packets.items():
        if psc < 256:
            print(f"Removing psc {psc} and inserting as {psc + MAX_PSC}")
            packet = packets.pop(psc)
            # Reinsert the popped packet with a PSC that will allow it to be sorted correctly.  Note that this doesn't
            # impact the underlying data, just the ordering for writing out the data. The end result should be
            # properly sorted packets with the PSC rollover accounted for.
            packets[psc + MAX_PSC] = packet
    return packets


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
            # TODO: Preserve hosc_hdr in output file
            hosc_hdr = in_file.read(HOSC_HEADER_SIZE)
            pkt = dp.CCSDSPacket(in_file)
            # print(pkt)

            # Get course time, fine, time and psc to sort packets
            course_time = int.from_bytes(pkt.body[:4], "big")
            fine_time = pkt.body[4]
            psc = pkt.pkt_seq_cnt
            print(f"<course={course_time} fine={fine_time} psc={psc}>")

            # Create a time_key index by combining padded course and fine times. This allows for sorting at the level
            # of course and fine time.  PSCs will be further sorted after accounting for PSC rollover
            time_key = str(course_time).zfill(10) + str(fine_time).zfill(3)
            # print(f"time_key: {time_key}")

            # Insert packets into SortedDict by time_key.  Use a sub-dictionary to track PSC max and min values within
            # a given time_key index. Also use another SortedDict to store packets indexed by PSC.  The
            # "sort_packets_by_psc" function sorts packets in cases where PSC rollovers occur for a given time_key index
            if time_key in pkts:
                min_psc = min(psc, pkts[time_key]["min"])
                max_psc = max(psc, pkts[time_key]["max"])
                pkts[time_key]["min"] = min_psc
                pkts[time_key]["max"] = max_psc
                pkts[time_key]["pkts"][psc] = pkt
                if max_psc - min_psc > 256:
                    pkts[time_key]["pkts"] = sort_packets_by_psc(pkts[time_key]["pkts"])
            else:
                pkts[time_key] = {
                    "min": psc,
                    "max": psc,
                    "pkts": SortedDict()
                }
                pkts[time_key]["pkts"][psc] = pkt

            cnt += 1
        except EOFError:
            break

    print(f"Count: {cnt}")

    # Iterate over pkts and its sub-dictionary and write out packets in sorted order
    with open(args.input_file.replace(".bin", "_sorted.bin"), "wb") as outfile:
        for time, packets in pkts.items():
            for psc, pkt in packets["pkts"].items():
                print(f"{time}: {psc}")
                outfile.write(HOSC_HEADER)
                outfile.write(pkt.hdr_data)
                outfile.write(pkt.body)


if __name__ == "__main__":
    main()