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

from constants import DEFAULT_LIB, AUDIO_FORMATS
from user_preferences import naming_format
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


def move_audio(audio, library, verbose, dry_run):
    """
    Copy audio to library.
    """
    try:
        # tag values are stored in lists so we unpack them here:
        tags = { k:v[0] for (k,v) in read_tags(audio).iteritems() }
    except ID3NoHeaderError:
        print("Error: {} has no ID3 tags. Moving on to next file.".format(audio))
        return

    # TODO this is ugly!
    tags['ext'] = os.path.splitext(audio)[1]
    tags['zero_padding'] = zero_padding
    dest = naming_format.format(**tags)

    
    if verbose or dry_run:
        print('Copying {} to {}.'.format(audio, dest))
    if not dry_run: 
        shutil.copy2(audio, dest)
        if not compare_files(audio, dest):
            print('Error in copying {} from {}. Moving on to next ' \ 
                  'file'.format(audio, dest))


def organize_files(folder, library, copy_non_audio, 
                   verbose=False, dry_run=False):
    """
    Move all audio files in folder (not including its subdirectories) 
    to the user's music library.

    folder - full path to directory containing audio files
    library - full path to music library to copy files to
    copy_non_audio - whether to copy non-audio files from folder to library
    verbose - enable status messages to be printed
    dry_run - print status messages, WITHOUT copying anything
    """ 
    songs = [ os.path.join(folder, f) for f in os.listdir(folder) 
              if os.path.isfile(os.path.join(folder, f)) 
              and os.path.splitext(f)[1].lower() in AUDIO_FORMATS ]

    for f in songs:
        move_audio(f, library, verbose, dry_run)

    if copy_non_audio:
        others = [ os.path.join(folder, f) for f in os.listdir(folder)
                   if os.path.isfile(os.path.join(folder, f))
                   and os.path.splitext(f)[1].lower() not in audio_formats ]
        for o in others:
            move_non_audio(o, library)

def main():
    p = argparse.ArgumentParser(description='Reorganize music files ' \
        'according to their tags.')
    p.add_argument('folders', metavar='folders', type=str, nargs='+', 
                   help='folders with music to be organized')
    p.add_argument('-l', '--library', help='path to music library', 
                   default=DEFAULT_LIB)
    p.add_argument('-c', '--copy_non_audio', 
                   help='copy non-audio files into library (i.e. album art, ' \
                   'audio rip report files from programs like EAC)',
                   action='store_true')
    p.add_argument('-v', '--verbose', help='output detailed status messages',
                   action='store_true')
    p.add_argument('-d', '--dryrun', help='output paths to copy files to, ' \
                   'without actually copying them; used for test purposes, ' \
                   'equivalent to --verbose without copying',
                   action='store_true')
    args = p.parse_args()

    if args.dryrun:
        print('--dryrun enabled; nothing will actually be copied')

    for f in args.folders:
        organize_files(f, args.library, args.copy_non_audio, args.verbose,
                       args.dryrun)


if __name__ == '__main__':
    main()

