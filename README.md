photocopy
=========

A script to archive photos off a camera or directory to a directory named by file date. 
It will prefer to use the EXIF date in the file. If not present it will skip file unless the flag `-x no` 
(do not skip files without EXIF date) is passed in which case it will use file system creation date. All operations
are logged into the target directory in a text file. 

Installation
------------

Just run:

    pip install docopt

    pip install hachoir

    Then execute the script using python.

To install the software. You're ready to use it!


Usage
-----
What photocopy does is read the EXIF data from images and copy the latter to a
specified directory. The use case is that you have an SD card from your camera
and want to copy all the images/videos into specific directories by day or
month.

You run it with:

    ./photocopy.py /media/sdcard/ /home/user/Photos/

and it will copy the photos to directories called "2014_03_12" by default.
See the source file for more examples.


Examples of log entries
------------------------

#### Plain info logging

![Plain log](../master/doc/log01.png)


#### Debug, verbose logging

![Debug log](../master/doc/log1.png)



 File Formats
 -------------

This version of photocopy uses the hachoir software to extract EXIF metadata. Hachoir supports the following 
file formats as of version 3.1.3 in February 2021.

#### Archive
 *  bzip2: bzip2 archive
 *  cab: Microsoft Cabinet archive
 *  gzip: gzip archive
 *  mar: Microsoft Archive
 *  tar: TAR archive
 *  zip: ZIP archive
#### Audio
 *  aiff: Audio Interchange File Format (AIFF)
 *  mpeg_audio: MPEG audio version 1, 2, 2.5
 *  real_audio: Real audio (.ra)
 *  sun_next_snd: Sun/NeXT audio
#### Container
 *  matroska: Matroska multimedia container
 *  ogg: Ogg multimedia container
 *  real_media: !RealMedia (rm) Container File
 *  riff: Microsoft RIFF container
#### Image
 *  bmp: Microsoft bitmap (BMP) picture
 *  gif: GIF picture
 *  ico: Microsoft Windows icon or cursor
 *  jpeg: JPEG picture
 *  pcx: PC Paintbrush (PCX) picture
 *  png: Portable Network Graphics (PNG) picture
 *  psd: Photoshop (PSD) picture
 *  targa: Truevision Targa Graphic (TGA)
 *  tiff: TIFF picture
 *  wmf: Microsoft Windows Metafile (WMF)
 *  xcf: Gimp (XCF) picture
#### Misc
 *  ole2: Microsoft Office document
 *  pcf: X11 Portable Compiled Font (pcf)
 *  torrent: Torrent metainfo file
 *  ttf: !TrueType font
#### Program
 *  exe: Microsoft Windows Portable Executable
#### Video
 *  asf: Advanced Streaming Format (ASF), used for WMV (video) and WMA (audio)
 *  flv: Macromedia Flash video
 *  mov: Apple !QuickTime movie
 *  mp4: [seems to work too]

