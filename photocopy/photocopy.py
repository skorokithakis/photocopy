#!/usr/bin/env python
"""Usage:
  photocopy.py [options] <source_dir> <destination_dir>

Options:
  -h --help                show this help and exit
  -v --version             show version and exit
  -d --dry-run             show what will happen
  -f --date-format=FORMAT  the date format to use [default: %Y-%M-%D]
     --verbose             talk more
"""

import datetime
import exifread
import logging
import os
import re
import sys
import shutil

from docopt import docopt

logger = logging.getLogger(__name__)


def set_up_logging(arguments):
    if arguments["--verbose"]:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_created_date(filename):
    if re.search("\.(jpeg|jpg|cr2)$", filename.lower()):
        image = open(filename, "rb")
        tags = exifread.process_file(image, details=False, stop_tag="Image DateTime")
        created_date = datetime.datetime.strptime(tags["Image DateTime"].values, "%Y:%m:%d %H:%M:%S")
    else:
        created_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    return created_date


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    arguments = docopt(__doc__, argv=args, version="0.0.1")
    set_up_logging(arguments)

    source_dir = arguments["<source_dir>"]
    destination_dir = arguments["<destination_dir>"]

    for file in os.listdir(source_dir):
        source = os.path.join(source_dir, file)
        logger.debug("Examining %s..." % source)

        created_date = get_created_date(source)
        logger.debug("Creation date is %s." % created_date)

        destination = os.path.join(destination_dir, created_date.strftime(arguments["--date-format"]))
        if not os.path.isdir(destination) and not arguments.get("--dry-run"):
            os.makedirs(destination)
        logger.info("Moving %s to %s..." % (source, destination))
        if not arguments.get("--dry-run"):
            shutil.move(source, destination)


if __name__ == "__main__":
    main()
