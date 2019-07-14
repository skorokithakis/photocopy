photocopy
=========

A script to archive photos off a camera to a directory.

Installation
------------

Just run:

    pip install photocopy

To install the software. You're ready to use it!


Usage
-----
What photocopy does is read the EXIF data from images and copy the latter to a
specified directory. The use case is that you have an SD card from your camera
and want to copy all the images/videos into specific directories by day or
month.

You run it with:

    ./photocopy.py /media/sdcard/ /home/user/Photos/

and it will copy the photos to directories called "2014-03-12" by default.
