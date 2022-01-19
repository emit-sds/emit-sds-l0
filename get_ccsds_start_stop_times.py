#!/usr/bin/env python
import argparse
import datetime
import json

from ait.core import log
from ait.core import dmc

import emit.data_products as dp


def main():
    parser = argparse.ArgumentParser(
        description="Get the start and stop times of the input CCSDS stream file"
    )

    parser.add_argument(
        "input_path",
        help="File from which CCSDS data will be read",
    )

    parser.add_argument(
        "output_path",
        help="Output path where to write start/stop values in JSON format",
    )

    args = parser.parse_args()

    start_time = None
    stop_time = None

    with open(args.input_path, "rb") as f:
        while True:
            try:
                # Read a packet
                pkt = dp.CCSDSPacket(stream=f)
                # Get coarse time and convert to UTC
                coarse_time = int.from_bytes(pkt.body[:4], "big")
                d = dmc.GPS_Epoch + datetime.timedelta(seconds=coarse_time)
                offset = dmc.LeapSeconds.get_GPS_offset_for_date(d)
                utc_time = d - datetime.timedelta(seconds=offset)

                if start_time is None:
                    start_time = utc_time
                    log.info(f"Start Time: {start_time}")

                stop_time = utc_time
            except EOFError:
                log.info(
                    "Received EOFError when reading file. No more packets to process."
                )
                break

    log.info(f"Stop Time: {stop_time}")

    output = {
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stop_time": stop_time.strftime("%Y-%m-%dT%H:%M:%S")}

    with open(args.output_path, "w") as f:
        json.dump(output, f)


if __name__ == "__main__":
    main()
