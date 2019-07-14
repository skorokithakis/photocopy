#!/usr/bin/env python
"""Usage:
  photocopy.py [options] <source_dir> <destination_dir>

Options:
  -h --help                Show this help and exit.
     --version             Show version and exit.
  -d --dry-run             Show what will happen.
  -j --ignore-jpg          Ignore (or delete when moving) JPG files when a RAW file with the same name exists.
  -e --event=EVENT         The name of the event in the photos. A subdirectory will be created for this event in the
                           original directory.
  -m --move                Move files instead of copying.
  -f --date-format=FORMAT  The date format to use [default: %Y-%m-%d].
  -v --verbose             Talk more.
"""

import datetime
import glob
import logging
import os
import re
import shutil
import sys

import exifread
from docopt import docopt

from .version import VERSION

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = ("cr2", "arw", "dng")


def set_up_logging(arguments):
    if arguments["--verbose"]:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_created_date(filename):
    created_date = None
    if re.search("\.(jpeg|jpg|%s)$" % "|".join(RAW_EXTENSIONS), filename.lower()):
        logger.debug("  File probably has an EXIF tag, checking...")
        image = open(filename, "rb")
        tags = exifread.process_file(image, details=False, stop_tag="Image DateTime")
        read_date = (
            tags["Image DateTime"].values
            or tags["EXIF DateTimeOriginal"].values
            or tags["EXIF DateTimeDigitized"].values
        )
        if read_date:
            created_date = datetime.datetime.strptime(read_date, "%Y:%m:%d %H:%M:%S")

    if not created_date:
        created_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    return created_date


def file_sorting_key(filename):
    """
    Extract a key for a filename sort, putting JPEGs before everything else.
    """
    extension = filename.lower()[filename.rfind(".") + 1 :]
    key = 0 if extension in ("jpg", "jpeg") else 1
    return (key, filename)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    arguments = docopt(__doc__, argv=args, version=VERSION)
    set_up_logging(arguments)

    source_dir = arguments["<source_dir>"]
    destination_dir = arguments["<destination_dir>"]
    files_in_source = sorted(os.listdir(source_dir), key=file_sorting_key)

    for file in files_in_source:
        file_extension = file[file.rfind(".") + 1 :].lower()
        source = os.path.join(source_dir, file)
        logger.debug("Examining %s..." % source)

        if arguments["--ignore-jpg"] and file_extension in ("jpg", "jpeg"):
            # Discover other files with the same extension.
            files = glob.glob(source[: source.rfind(".")] + ".*")
            extensions = [fn[-3:].lower() for fn in files]
            if any(extension in RAW_EXTENSIONS for extension in extensions):
                if arguments.get("--move"):
                    logger.debug("  Deleting file because another RAW file exists.")
                    if not arguments.get("--dry-run"):
                        os.remove(source)
                else:
                    logger.debug("  Skipping file because another RAW file exists.")
                continue

        created_date = get_created_date(source)
        logger.debug("  Creation date is %s." % created_date)

        destination = os.path.join(
            destination_dir, created_date.strftime(arguments["--date-format"])
        )
        if arguments["--event"]:
            destination = os.path.join(destination, arguments["--event"])
        if not os.path.isdir(destination) and not arguments.get("--dry-run"):
            os.makedirs(destination)

        dest_filename = os.path.join(destination, os.path.basename(source))
        if os.path.exists(dest_filename):
            logger.info(
                "  Destination file %s already exists, skipping." % dest_filename
            )
            continue

        if arguments.get("--move"):
            logger.info("  Moving: %s -> %s..." % (source, destination))
            if not arguments.get("--dry-run"):
                shutil.move(source, destination)
        else:
            logger.info("  Copying: %s -> %s..." % (source, destination))
            if not arguments.get("--dry-run"):
                shutil.copy(source, destination)


if __name__ == "__main__":
    main()
