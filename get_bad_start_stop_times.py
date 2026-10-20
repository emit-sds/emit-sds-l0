#!/usr/bin/env python
import argparse
import csv
import datetime
import json

from argparse import RawTextHelpFormatter

GPS_EPOCH = datetime.datetime(1980, 1, 6)
GPS_UTC_OFFSET = 18


def get_utc_time_from_gps(gps_time):
    # Convert gps_time in seconds to a timestamp in utc
    d = GPS_EPOCH + datetime.timedelta(seconds=gps_time)
    utc_time = d - datetime.timedelta(seconds=GPS_UTC_OFFSET)
    return utc_time


def main():
    parser = argparse.ArgumentParser(
        description="Description: This script gets the start and stop times of the input BAD stream file.\n"
                    "Operating Environment: Python 3.x. See setup.py file for specific dependencies.\n"
                    "Outputs:\n"
                    "    * A JSON formatted file containing start and stop times.\n",
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        "input_path",
        help="CSV file from which BAD data will be read",
    )

    parser.add_argument(
        "output_path",
        help="Output path where to write start/stop values in JSON format",
    )

    args = parser.parse_args()

    with open(args.input_path, newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        headers = next(reader)
        rows = list(reader)

    index = None
    for i, header in enumerate(headers):
        # LADP06MD2378W is the header for the coarse time (in GPS seconds)
        if header == "LADP06MD2378W":
            index = i
            break

    if index is None:
        raise RuntimeError("Unable to find coarse time column (LADP06MD2378W) in data")

    gps_times = [float(row[index]) for row in rows if len(row) > index and float(row[index]) > 0]

    start_time = get_utc_time_from_gps(min(gps_times))
    stop_time = get_utc_time_from_gps(max(gps_times))

    output = {
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stop_time": stop_time.strftime("%Y-%m-%dT%H:%M:%S")}

    with open(args.output_path, "w") as f:
        json.dump(output, f)


if __name__ == "__main__":
    main()
