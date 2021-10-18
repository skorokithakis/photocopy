photocopy
=========

A script to archive photos off a camera or directory to a directory named by file date. 
It will prefer to use the EXIF date in the file. If not present it will skip file unless the flag `-x no` 
(do not skip files without EXIF date) is passed in which case it will use file system creation date. All operations
are logged into the target directory in a text file. 

Installation
------------

Just run:

    1. Clone down the repo, or just download `photocopy.py`
    2. pip install docopt
    3. pip install hachoir
    4. Then execute the script using python.

You're ready to use it!


Usage
-----
Photocopy recursively reads the EXIF data from images and other file types (see below) in source directory and copies the files to a
specified target directory with subdirectories for the creation dates of the files. It does not rename files. A use case is that 
you have an SD card from your camera, or a folder from a remote syncing service, and want to copy all the images/videos into specific 
directories by day.

You run it with:

    ./photocopy.py /media/sdcard/ /home/user/Photos/
    
 #### Examples:
    
 1. Simple. Copy jpg or JPG files from source (Z:\photosync) to target into folders
       named YYYY_MM_DD using the EXIF Creation Date in the JPG files. Ignore files without
       EXIF date, but log everything.
       
        `# python photocopy.py -j jpg Z:\photosync target/`
        
2. More complex. Move (-m yes) files by extensions shown from source (Z:\photosync) to target into folders   
        named YYYY_MM_DD using the EXIF Creation Date in the files. File without EXIF date will use the file
        system creation date to name target folders. Log everything.
        
        `# python photocopy.py -m yes -x no -j gif,png,jpg,mov,mp4 Z:\photosync target/`

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

