#!/usr/bin/env python
"""Usage:
  photocopy.py [options] <source_dir> <destination_dir>

Options:
  -h --help                show this help and exit
  -v --version             show version and exit
  -d --dry-run             show what will happen
  -f --date-format=FORMAT  the date format to use [default: %Y-%M-%D]
"""

import datetime
import exifread
import os
import shutil

from docopt import docopt


def main(arguments):
    source_dir = arguments["<source_dir>"]
    destination_dir = arguments["<destination_dir>"]

    for file in os.listdir(source_dir):
        source = os.path.join(source_dir, file)
        image = open(source, "rb")
        tags = exifread.process_file(image, details=False, stop_tag="Image DateTime")
        date = datetime.datetime.strptime(tags["Image DateTime"].values, "%Y:%m:%d %H:%M:%S")
        destination = os.path.join(destination_dir, date.strftime(arguments["--date-format"]))
        if not os.path.isdir(destination):
            os.makedirs(destination)
        print "Moving %s to %s..." % (source, destination)
        if not arguments.get("--dry-run"):
            shutil.move(source, destination)


if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.0.1")
    main(arguments)
