# Input: directory name
# Output: Rearranged directory structure. Each audio file in the directory should be reorganized according to the following structure:
# "song" by artist on album should be in ArtistName/AlbumName/tracknum - song.mp3

import os
import os.path
import shutil
import sys

from mutagen.flac import FLAC
from mutagen.m4a import M4A
from mutagen.mp3 import EasyMP3


def move_mp3(mp3):
    """
    Move the file into its proper directory, according to path.
    
    mp3 - full path to an MP3 file
    """
    # TODO
    pass


def organize_files(folder):
    """
    Moves all audio files in folder to the user's music library.

    folder - full path to folder containing audio files
    """

    files = [ os.path.join(folder, f) for f in os.listdir(folder) 
              if os.path.isfile(os.path.join(folder, f)) ]
    for f in files:
        if f.lower().endswith('.flac'):
            # TODO
            pass
        elif f.lower().endswith('.m4a'):
            # Keys for tags:
            # 'cpil': Is this track part of a compilation?
            # 'disk': (on disk #, of # disks)
            # 'purd': purchase date
            # 'soal': song album
            # 'soar': song artist
            # 'sonm': song title
            # 'trkn': (track #, out of #)
            # TODO
            pass
        elif f.lower().endswith('.mp3'):
            # Keys for EasyMP3 tags:
            # 'album' - str list; album name
            # 'performer' - str list; is this album artist or regular artist or what?
            # 'artist' - str list; see above
            # 'title' - str list; the song's title
            # 'date' - str list; date the song was released
            # 'tracknumber' - str list; track #
            # 'disknumber' - str list; disk #
            audio = EasyMP3(f)
            # TODO change this to use os.path.join later on!
            # function to make file name might be useful too? or function that takes constructor name and filename and does this work in it?
            # new_path = u'/Users/eric/Music/' + audio[u'artist'][0] + '/' + audio[u'album'][0] + '/' + audio[u'tracknumber'][0].zfill(2) + '-' + audio[u'title'][0] + '.mp3'
            new_path = os.path.join('/Users/eric/Music', audio[u'artist'][0], 
                                    audio[u'album'][0])
            #TODO make nicer
            new path += audio[u'tracknumber'][0].zfill(2) + '-' + audio[u'title'][0] + '.mp3'
            if not os.path.isdir(os.path.abspath(os.path.join(new_path, os.pardir))):
                os.makedirs(os.path.abspath(os.path.join(new_path, os.pardir)))
            
            shutil.move(os.path.join(folder, f), new_path)


def main():
    print sys.argv[1]
    organize_files(sys.argv[1])

if __name__ == '__main__':
    main()
