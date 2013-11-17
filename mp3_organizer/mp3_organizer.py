# Input: directory name
# Output: Rearranged directory structure. Each audio file in the directory should be reorganized according to the following structure:
# "song" by artist on album should be in ArtistName/AlbumName/tracknum - song.mp3
# Future Improvements (in order of expected difficulty, ascending):
# Config file - user enters their main music folder into it, along with the user's chosen naming structure
# Customizable naming/directory structure scheme.
# Updating iTunes/Winamp/etc. databases.
# Automatic correction of album titles/capitalization (The vs the, etc.)
# Automatically tagging files.

import os
import os.path
import sys

from mutagen.flac import FLAC
from mutagen.m4a import M4A
from mutagen.mp3 import MP3

# Possibly Useful keys for tags:
# 'cpil': Is this track part of a compilation?
# 'disk': (on disk #, of # disks)
# 'purd': purchase date
# 'soal': song album
# 'soar': song artist
# 'sonm': song title
# 'trkn': (track #, out of #)

music_path = sys.argv[1]

# For file in directory (how do we handle subdirectories? should files in them be considered too?)
# Get file's extension.
# Open it using the proper constructor (FLAC/M4A/MP3 as above)
# Move it to the right folder and rename it (creating necessary folders if need be)

def organize_files(folder):
    directory = os.listdir(folder)
    for f in directory:
        if os.path.isfile(os.path.join(folder, f)):
            if f.lower().endswith('.flac'):
                print 'FLAC'
            elif f.lower().endswith('.m4a'):
                print 'M4A'
            elif f.lower().endswith('.mp3'):
                print 'MP3'

def main():
    print sys.argv[1]
    organize_files(sys.argv[1])

if __name__ == '__main__':
    main()
