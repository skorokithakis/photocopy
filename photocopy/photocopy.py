#!/usr/bin/env python
usage = """Usage:
  photocopy.py [options] <source_dir> <destination_dir>

Options:
  -h --help                Show this help and exit.
  -j --extense=str         Extention list - comma separated [default: jpeg,jpg]. Supports all extensions of hachoir
  -m --move=str            move files (--move=yes) or copy (--move=no) [default: no, copy instead]
  -v --verbose             Talk more.
  -x --exifOnly=str        skip file processing if no EXIF (--exifOnly =yes)
                           or process files with no EXIF (--exifOnly =no)
                           or Only process files with no EXIF (--exifOnly =fs) [default: yes]

Examples:
    1. Simple. Copy jpg or JPG files from source (Z:\photosync) to target into folders
       named YYYY_MM_DD using the EXIF Creation Date in the JPG files. Ignore files without
       EXIF date, but log everything.
        # python photocopy.py -j jpg Z:\photosync target/

    2. More complex. Move (-m yes) files by extensions shown from source (Z:\photosync) to target into folders   
        named YYYY_MM_DD using the EXIF Creation Date in the files. File without EXIF date will use the file
        system creation date to name target folders. Log everything.
        # python photocopy.py -m yes -x no -j gif,png,jpg,mov,mp4 Z:\photosync target/
"""

import datetime
import logging
import os
import sys
import shutil

from docopt import docopt

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core import config

config.quiet = True

logger = logging.getLogger(__name__)

destination_dir = ""
extList = []
actMove = "no"
exifOnly = ""


def set_up_logging(arguments):
    if arguments["--verbose"]:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logfile = os.path.join(destination_dir, "events.log")
    logger.setLevel(level)
    ch = logging.FileHandler(logfile)
    ch.setLevel(level)
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_created_date(filename):
    created_date = None
    parser = createParser(filename)
    if not parser:
        logger.debug("Unable to parse file")

    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            logger.debug("Metadata extraction error: %s" % err)
            metadata = None
        if not metadata:
            logger.debug("Unable to extract metadata")
        else:
            cd = metadata.getValues("creation_date")
            if len(cd) > 0:
                created_date = cd[0]
    return created_date


def main(args=None):
    global destination_dir, extList, actMove, exifOnly
    if args is None:
        args = sys.argv[1:]
    arguments = docopt(usage)

    # get file extensions from options
    extensions = arguments["--extense"]
    extList = extensions.split(",")
    extList[:] = ["." + x for x in extList]
    # Options flags
    actMove = arguments["--move"]
    exifOnly = arguments["--exifOnly"]

    source_dir = arguments["<source_dir>"]
    destination_dir = arguments["<destination_dir>"]
    set_up_logging(arguments)
    # job started
    logger.info(
        50 * "-" + " Started: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )
    logger.debug("options: " + str(arguments))
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)
        logger.info("created: " + destination_dir)
    if os.path.isdir(source_dir):
        # main recursive function to process files
        recursive_walk(source_dir)
    else:
        logger.info("source dir not exists: " + source_dir)
    # job ended
    logger.info(
        70 * "-" + "Ended: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )
    logging.shutdown()


def recursive_walk(folder):
    for folderName, subfolders, filenames in os.walk(folder):
        logger.info("Folder: " + folderName)
        for filename in filenames:
            file_details = os.path.splitext(filename)
            file_extension = file_details[1].lower()
            # process only files with given extensions
            if file_extension in extList:
                moveFile(folderName, filename)
        if subfolders:  # process nested folders
            for subfolder in subfolders:
                recursive_walk(subfolder)


def moveFile(folder, filename):
    fullpath = os.path.join(folder, filename)
    cd = get_created_date(fullpath)
    comment = 9 * " "
    if not cd:
        cd = datetime.datetime.fromtimestamp(os.path.getmtime(fullpath))
        comment = " no EXIF "
    created_date = cd.strftime("%Y_%m_%d")
    space = 40 - len(filename)
    if space <= 0:
        space = 4
    destf = os.path.join(destination_dir, created_date)
    if not comment.isspace() and exifOnly == "yes":  # skip file processing
        logger.info(f"  {filename}  {comment:>{space}}    skipped")
    else:

        flagM = "moved" if actMove == "yes" else "copied"
        if (
            exifOnly == "no"
            or (exifOnly == "yes" and comment.isspace())
            or (exifOnly == "fs" and not comment.isspace())
        ):  # select by
            if not os.path.isdir(destf):  # create subdir to c/move
                os.makedirs(destf)
                logger.info("created new destination subdir: " + destf)
            if not os.path.exists(os.path.join(destf, filename)):
                if actMove == "yes":
                    shutil.move(fullpath, destf)
                else:
                    shutil.copy2(fullpath, destf)
                # logger.info('copy/move error' + error)
                logger.info(
                    f"  {filename}  {comment:>{space}}  {str(cd)} {flagM:>3} {destf}"
                )
            else:
                logger.info("  " + filename + " already exists in " + destf)
        elif exifOnly == "fs" and comment.isspace():
            logger.info(f"  {filename}  {comment:>{space}}    skipped")


if __name__ == "__main__":
    main()
