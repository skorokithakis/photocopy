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

and it will copy the photos to directories called "2014-03-12" by default.
See the source file for more examples.


Examples of log entries
------------------------

#### Plain info logging
----------------------------------------PhotoCopy version:1.0 Started: 2021/10/14 14:06:39
Folder: Z:photosync
Folder: Z:photosync\iPhone
Folder: Z:photosync\iPhone\PhotoSync
created new destination subdir: target/2021_08_23
  IMG_6981.mov                                2021-08-23 18:42:23 copied target/2021_08_23
Folder: Z:photosync\iPhone\Recents
created new destination subdir: target/2021_09_09
  65290110486__1175F04C-E756-4903-BF56-3261BA75BA49.JPG             2021-09-09 13:25:04 copied target/2021_09_09
  65290110486__1175F04C-E756-4903-BF56-3261BA75BA49.MOV             2021-09-09 17:25:04 copied target/2021_09_09
  65290731478__2DD52CCB-D29B-426B-ABAC-95969EA5F3AC.JPG             2021-09-09 15:08:34 copied target/2021_09_09
  65290731478__2DD52CCB-D29B-426B-ABAC-95969EA5F3AC.MOV             2021-09-09 19:08:34 copied target/2021_09_09
created new destination subdir: target/2021_10_01
  IMG_0002.JPG                                2021-10-01 15:39:13 copied target/2021_10_01
  IMG_0002.MOV                                2021-10-01 19:39:14 copied target/2021_10_01
created new destination subdir: target/2021_10_02
  IMG_0003.MOV                                2021-10-02 03:08:11 copied target/2021_10_02
  IMG_0004.PNG                      no EXIF     skipped
  IMG_0005.PNG                      no EXIF     skipped
  IMG_0006.JPG                                2021-10-02 07:21:22 copied target/2021_10_02
  IMG_0007.JPG                                2021-10-02 07:21:28 copied target/2021_10_02
  IMG_0007.MOV                                2021-10-02 11:21:28 copied target/2021_10_02
  IMG_0008.JPG                                2021-10-02 08:04:43 copied target/2021_10_02
  IMG_0008.MOV                                2021-10-02 12:04:43 copied target/2021_10_02
  IMG_0009.JPG                                2021-10-02 08:05:04 copied target/2021_10_02
  Folder: Z:photosync\iPhone\Recents
  IMG_0004.PNG already exists in target/2021_10_02
  IMG_0005.PNG already exists in target/2021_10_02
  IMG_6982.PNG already exists in target/2021_08_24
  IMG_6983.PNG already exists in target/2021_08_24
  ----------------------------------------------------------------------Ended: 2021/10/14  14:06:41

#### Debug, verbose logging
  ----------------------------------------PhotoCopy version:1.0 Started: 2021/10/14 15:14:44
options: {'--date-format': '%Y-%m-%d',
 '--exifOnly': 'no',
 '--extense': 'png',
 '--help': False,
 '--move': 'no',
 '--verbose': True,
 '--version': '1.0',
 '<destination_dir>': 'target/',
 '<source_dir>': 'Z:photosync'}
Folder: Z:photosync
  0000JZASTROW-LTP10.png already exists in target/2021_10_14
Folder: Z:photosync\iPhone
Folder: Z:photosync\iPhone\PhotoSync
Folder: Z:photosync\iPhone\Recents
  IMG_0004.PNG already exists in target/2021_10_02
  IMG_0005.PNG already exists in target/2021_10_02
  IMG_6982.PNG already exists in target/2021_08_24
 ----------------------------------------------------------------------Ended: 2021/10/14 15:14:50


 File Formats
 -------------

This version of photocopy uses the hachoir software to extract EXIF metadata. Hachoir supports the following 
file formats as of version 3.1.3 in February 2021.

#### Archive
• bzip2: bzip2 archive
• cab: Microsoft Cabinet archive
• gzip: gzip archive
• mar: Microsoft Archive
• tar: TAR archive
• zip: ZIP archive
#### Audio
• aiff: Audio Interchange File Format (AIFF)
• mpeg_audio: MPEG audio version 1, 2, 2.5
• real_audio: Real audio (.ra)
• sun_next_snd: Sun/NeXT audio
#### Container
• matroska: Matroska multimedia container
• ogg: Ogg multimedia container
• real_media: !RealMedia (rm) Container File
• riff: Microsoft RIFF container
#### Image
• bmp: Microsoft bitmap (BMP) picture
• gif: GIF picture
• ico: Microsoft Windows icon or cursor
• jpeg: JPEG picture
• pcx: PC Paintbrush (PCX) picture
• png: Portable Network Graphics (PNG) picture
• psd: Photoshop (PSD) picture
• targa: Truevision Targa Graphic (TGA)
• tiff: TIFF picture
• wmf: Microsoft Windows Metafile (WMF)
• xcf: Gimp (XCF) picture
#### Misc
• ole2: Microsoft Office document
• pcf: X11 Portable Compiled Font (pcf)
• torrent: Torrent metainfo file
• ttf: !TrueType font
#### Program
• exe: Microsoft Windows Portable Executable
#### Video
• asf: Advanced Streaming Format (ASF), used for WMV (video) and WMA (audio)
• flv: Macromedia Flash video
• mov: Apple !QuickTime movie
• mp4: [seems to work too]

