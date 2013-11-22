# Input: directory name
# Output: Rearranged directory structure. Each audio file in the directory should be reorganized according to the following structure:
# "song" by artist on album should be in ArtistName/AlbumName/tracknum - song.mp3

from __future__ import print_function
import hashlib
import os
import os.path
import shutil
import sys

from mutagen.flac import FLAC
from mutagen.m4a import M4A
from mutagen.mp3 import EasyMP3


def compare_files(f1, f2):
    """
    Compare two files for equality by comparing their SHA256 hashes.
    """
    # TODO make usable for an arbitrary number of files. idea - make a 
    # class inheriting file that overrides __eq__.
    # OTHER TODO: benchmark this
    hash_1 = hashlib.sha256()
    hash_2 = hashlib.sha256()

    with open(f1, 'rb') as f:
        cur_chunk = f.read(128)

        while len(cur_chunk) > 0:
            hash_1.update(cur_chunk)
            cur_chunk = f.read(128)

    with open(f2, 'rb') as f:
        cur_chunk = f.read(128)

        while len(cur_chunk) > 0:
            hash_2.update(cur_chunk)
            cur_chunk = f.read(128)
    
    return hash_1.hexdigest() == hash_2.hexdigest()

def move_flac(flac):
    # TODO
    pass


def move_m4a(m4a):
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


def move_mp3(mp3):
    """
    Move the file into its proper directory, according to path.
    
    mp3 - full path to an MP3 file
    """
    # Keys for EasyMP3 tags:
    # 'album' - str list; album name
    # 'performer' - str list; is this album artist or regular artist or what?
    # 'artist' - str list; see above
    # 'title' - str list; the song's title
    # 'date' - str list; date the song was released
    # 'tracknumber' - str list; track #
    # 'disknumber' - str list; disk #
    audio = EasyMP3(mp3)
    track_dir = os.path.join('/Users/eric/Music', audio[u'artist'][0], 
                            audio[u'album'][0])
    track_name = audio[u'tracknumber'][0].zfill(2) + '-' + audio[u'title'][0] + '.mp3'
    new_track = os.path.join(track_dir, track_name)
    if not os.path.isdir(track_dir):
        os.makedirs(track_dir)
            
    shutil.copyfile(mp3, new_track)
    if compare_files(mp3, new_track):
        print('Copied {0} to {1} successfully.'.format(mp3, new_track))
    else:
        print('Moving {0} to {1} failed.'.format(mp3, new_track))


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
            move_flac(f)
        elif f.lower().endswith('.m4a'):
            move_m4a(f)
        elif f.lower().endswith('.mp3'):
            move_mp3(f)

def main():
    for folder in sys.argv[1:]:
        organize_files(folder)

if __name__ == '__main__':
    main()
