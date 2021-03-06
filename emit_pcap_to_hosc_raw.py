#!/usr/bin/env python
import argparse
import datetime
import io
import os.path
import shutil

from ait.core import log
from ait.core import pcap
from ait.core import dmc

import emit.data_products as dp

HOSC_HEADER = bytes(28)


def main():
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
    out_file_1676 = os.path.join(args.output_dir, "emit_1676_hsc.bin")

    pkt_cnt_1674 = 0
    pkt_cnt_1675 = 0
    pkt_cnt_1676 = 0

    start_time_1674 = 0
    start_time_1675 = 0
    start_time_1676 = 0
    stop_time_1674 = 0
    stop_time_1675 = 0
    stop_time_1676 = 0

    with pcap.open(input_file, "r") as infile:
        with open(out_file_1674, "wb") as outfile_1674, open(out_file_1675, "wb") as outfile_1675, \
                open(out_file_1676, "wb") as outfile_1676:
            for _header, data in infile:

                # Drop ethernet frame header and setup stream-like interface
                in_bytes = io.BytesIO(data[14:])

                # Our ethernet frames only contain a single CCSDS Packet ...
                pkt = dp.CCSDSPacket(stream=in_bytes)

                # Get coarse time and convert to UTC
                coarse_time = int.from_bytes(pkt.body[:4], "big")
                d = dmc.GPS_Epoch + datetime.timedelta(seconds=coarse_time)
                offset = dmc.LeapSeconds.get_GPS_offset_for_date(d)
                utc_time = d - datetime.timedelta(seconds=offset)

                # Write out HOSC files separately for engineering stream (APID 1674), science stream (APID 1675),
                # and engineering ancillary stream (APID 1676)
                if pkt.apid == 1674:
                    if pkt_cnt_1674 == 0:
                        start_time_1674 = utc_time
                        log.info(f"APID 1674 Start Time: {start_time_1674}")
                    stop_time_1674 = utc_time
                    outfile_1674.write(HOSC_HEADER)
                    outfile_1674.write(pkt.hdr_data)
                    outfile_1674.write(pkt.body)
                    pkt_cnt_1674 += 1
                elif pkt.apid == 1675:
                    if pkt_cnt_1675 == 0:
                        start_time_1675 = utc_time
                        log.info(f"APID 1675 Start Time: {start_time_1675}")
                    stop_time_1675 = utc_time
                    outfile_1675.write(HOSC_HEADER)
                    outfile_1675.write(pkt.hdr_data)
                    outfile_1675.write(pkt.body)
                    pkt_cnt_1675 += 1
                elif pkt.apid == 1676:
                    if pkt_cnt_1676 == 0:
                        start_time_1676 = utc_time
                        log.info(f"APID 1676 Start Time: {start_time_1676}")
                    stop_time_1676 = utc_time
                    outfile_1676.write(HOSC_HEADER)
                    outfile_1676.write(pkt.hdr_data)
                    outfile_1676.write(pkt.body)
                    pkt_cnt_1676 += 1

    # Rename output files using format "emit_<APID>_<START_TIME>_<STOP_TIME>_<CUR_TIME>_hsc.bin"
    current_utc_time = datetime.datetime.utcnow()

    log.info(f"Packet counts - 1674: {pkt_cnt_1674}, 1675: {pkt_cnt_1675}, 1676: {pkt_cnt_1676}")

    if pkt_cnt_1674 > 0:
        renamed_1674 = out_file_1674.replace("hsc.bin", "_".join([start_time_1674.strftime("%y%m%d%H%M%S"),
                                                                  stop_time_1674.strftime("%y%m%d%H%M%S"),
                                                                  current_utc_time.strftime("%y%m%d%H%M%S"),
                                                                  "hsc.bin"]))
        shutil.move(out_file_1674, renamed_1674)
        log.info(f"Wrote {pkt_cnt_1674} packets to {renamed_1674}")
    else:
        os.remove(out_file_1674)

    if pkt_cnt_1675 > 0:
        renamed_1675 = out_file_1675.replace("hsc.bin", "_".join([start_time_1675.strftime("%y%m%d%H%M%S"),
                                                                  stop_time_1675.strftime("%y%m%d%H%M%S"),
                                                                  current_utc_time.strftime("%y%m%d%H%M%S"),
                                                                  "hsc.bin"]))
        shutil.move(out_file_1675, renamed_1675)
        log.info(f"Wrote {pkt_cnt_1675} packets to {renamed_1675}")
    else:
        os.remove(out_file_1675)

    if pkt_cnt_1676 > 0:
        renamed_1676 = out_file_1676.replace("hsc.bin", "_".join([start_time_1676.strftime("%y%m%d%H%M%S"),
                                                                  stop_time_1676.strftime("%y%m%d%H%M%S"),
                                                                  current_utc_time.strftime("%y%m%d%H%M%S"),
                                                                  "hsc.bin"]))
        shutil.move(out_file_1676, renamed_1676)
        log.info(f"Wrote {pkt_cnt_1676} packets to {renamed_1676}")
    else:
        os.remove(out_file_1676)


if __name__ == "__main__":
    main()
