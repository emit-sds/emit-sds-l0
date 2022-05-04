#!/usr/bin/env python
import argparse
import csv
import datetime
import json

from argparse import RawTextHelpFormatter


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
        if header == "Timestamp : Embedded GMT":
            index = i
            break

    if index is None:
        raise RuntimeError("Unable to find embedded GMT column in data")

    timestamps = [datetime.datetime.strptime(row[index], "%Y:%j:%H:%M:%S") for row in rows]

    start_time = min(timestamps)
    stop_time = max(timestamps)

    output = {
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stop_time": stop_time.strftime("%Y-%m-%dT%H:%M:%S")}

    with open(args.output_path, "w") as f:
        json.dump(output, f)


if __name__ == "__main__":
    main()
