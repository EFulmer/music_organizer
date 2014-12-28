# music_organizer.py
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import hashlib
import os
import os.path
import shutil
import sys

from mutagenwrapper import read_tags

from constants import DEFAULT_LIB
from user_preferences import naming_style
from user_preferences import zero_padding


def compare_files(f1, f2):
    """
    Compare two files for equality by comparing their SHA256 hashes.
    """
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


def move_audio(audio):
    """"""

def organize_files(folder):
    """
    Move all audio files in folder (not including its subdirectories) 
    to the user's music library.

    folder - full path to directory containing audio files
    """
    
    songs = [ os.path.join(folder, f) for f in os.listdir(folder) 
              if os.path.isfile(os.path.join(folder, f)) 
              and os.path.splitext(f)[1] in audio_formats ]

    others = [ os.path.join(folder, f) for f in os.listdir(folder)
               if os.path.isfile(os.path.join(folder, f))
               and os.path.splitext(f)[0] not in audio_formats ]
    for f in songs:
        move_audio(f)


def main():
    p = argparse.ArgumentParser(description='Reorganize music files ' \
        'according to their tags.')
    p.add_argument('folders', metavar='folders', type=str, nargs='+', 
                   help='folders with music to be organized')
    p.add_argument('-v', '--verbose', help='output detailed status messages',
                   action='store_true')
    p.add_argument('-l', '--library', help='path to music library', 
                   default=DEFAULT_LIB)
    args = p.parse_args()
    print(args.folders)
    if args.verbose:
        print('verbose')
    else:
        print('not verbose')
    print(args.library)


if __name__ == '__main__':
    main()
