#!/usr/bin/env python
"""Usage:
  photocopy.py [options] <source_dir> <destination_dir>

Options:
  -h --help                Show this help and exit.
     --version             Show version and exit.
  -d --dry-run             Show what will happen.
  -e --event=EVENT         The name of the event in the photos. A subdirectory will be created for this event in the
                           original directory.
  -m --move                Move files instead of copying.
  -f --date-format=FORMAT  The date format to use [default: %Y-%m-%d].
  -v --verbose             Talk more.
"""

import datetime
import exifread
import logging
import os
import re
import sys
import shutil

from docopt import docopt
from .version import VERSION

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

    arguments = docopt(__doc__, argv=args, version=VERSION)
    set_up_logging(arguments)

    source_dir = arguments["<source_dir>"]
    destination_dir = arguments["<destination_dir>"]

    for file in os.listdir(source_dir):
        source = os.path.join(source_dir, file)
        logger.debug("Examining %s..." % source)

        created_date = get_created_date(source)
        logger.debug("Creation date is %s." % created_date)

        destination = os.path.join(destination_dir, created_date.strftime(arguments["--date-format"]))
        if arguments["--event"]:
            destination = os.path.join(destination, arguments["--event"])
        if not os.path.isdir(destination) and not arguments.get("--dry-run"):
            os.makedirs(destination)

        dest_filename = os.path.join(destination, os.path.basename(source))
        if os.path.exists(dest_filename):
            logger.info("Destination file %s already exists, skipping." % dest_filename)
            continue

        if arguments.get("--move"):
            logger.info("Moving: %s -> %s..." % (source, destination))
            if not arguments.get("--dry-run"):
                shutil.move(source, destination)
        else:
            logger.info("Copying: %s -> %s..." % (source, destination))
            if not arguments.get("--dry-run"):
                shutil.copy(source, destination)


if __name__ == "__main__":
    main()
