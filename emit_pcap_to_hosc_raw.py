#!/usr/bin/env python
import argparse
import io
import os.path

from ait.core import log
from ait.core import pcap

import emit.data_products as dp


HOSC_HEADER = bytes(28)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert raw Ethernet PCAPs into HOSC-like data files"
    )

    parser.add_argument(
        "--input-file",
        required=True,
        help="File from which Ethernet data will be read",
    )

    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where converted data will be written (default is current directory)",
    )

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    out_file_1674 = os.path.join(args.output_dir, "emit_1674_hsc.bin")
    out_file_1675 = os.path.join(args.output_dir, "emit_1675_hsc.bin")

    pkt_cnt_1674 = 0
    pkt_cnt_1675 = 0

    with pcap.open(input_file, "r") as infile:
        with open(out_file_1674, "wb") as outfile_1674, open(out_file_1675, "wb") as outfile_1675:
            for _header, data in infile:

                # Hopefully filter out any ethernet frames that aren't from EMIT
                if len(data) != 1514:
                    continue

                # Drop ethernet frame header and setup stream-like interface
                in_bytes = io.BytesIO(data[14:])

                # Our ethernet frames only contain a single CCSDS Packet ...
                pkt = dp.CCSDSPacket(stream=in_bytes)

                if pkt.apid == 1674:
                    outfile_1674.write(HOSC_HEADER)
                    outfile_1674.write(pkt.hdr_data)
                    outfile_1674.write(pkt.body)
                    pkt_cnt_1674 += 1
                elif pkt.apid == 1675:
                    outfile_1675.write(HOSC_HEADER)
                    outfile_1675.write(pkt.hdr_data)
                    outfile_1675.write(pkt.body)
                    pkt_cnt_1675 += 1

    log.info(f"Wrote {pkt_cnt_1674} packets to {out_file_1674}")
    log.info(f"Wrote {pkt_cnt_1675} packets to {out_file_1675}")