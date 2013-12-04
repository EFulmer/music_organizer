# Input: directory name
# Output: Rearranged directory structure.

from __future__ import print_function
import hashlib
import os
import os.path
import shutil
import sys

from mutagen.flac import FLAC
from mutagen.m4a import M4A
from mutagen.mp3 import EasyMP3

from user_preferences import naming_style
from user_preferences import zero_padding


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


def tags_to_names(fmt, tag_dict):
    """Convert the tag names from fmt to the names used to rename the music file."""
    names = {}
    names['ext'] = fmt
    names['zero_padding'] = zero_padding
    if fmt == 'flac':
        # TODO
        pass
    elif fmt == 'm4a':
        # Keys for tags:
        # 'cpil': Is this track part of a compilation?
        # 'disk': (on disk #, of # disks)
        # 'purd': purchase date
        # 'soal': song album
        # 'soar': song artist
        # 'sonm': song title
        # 'trkn': (track #, out of #)
        names['artist_name'] = tag_dict[u'soar']
        names['album_name'] = tag_dict[u'soal']
        names['track_num'] = tag_dict[u'trkn'][0]
        names['track_title'] = tag_dict[u'sonm']
        names['ext'] = fmt
        names['zero_padding'] = zero_padding
    elif fmt == 'mp3':
        # Keys for EasyMP3 tags:
        # 'album' - str list; album name
        # 'performer' - str list; is this album artist or regular artist or what?
        # 'artist' - str list; see above
        # 'title' - str list; the song's title
        # 'date' - str list; date the song was released
        # 'tracknumber' - str list; track #/total tracks
        # 'disknumber' - str list; disk #
        names['artist_name'] = tag_dict[u'artist'][0]
        names['album_name'] = tag_dict[u'album'][0]
        names['track_num'] = int(tag_dict[u'tracknumber'][0])
        names['track_title'] = tag_dict[u'title'][0]
        names['ext'] = fmt
        names['zero_padding'] = zero_padding
    else:
        raise ValueError('expected music format name')
    return names


# TODO can refactor these three functions into one that grabs 
# the ext (only takes the filename) and passes it to tags_to_names.
# refactor tags_to_names to actually open the file using the right 
# constructor and return the filename.
def move_flac(flac):
    # TODO
    pass


def move_m4a(m4a):
    """
    Move the file into its proper directory, according to path.
    
    mp3 - full path to an MP3 file
    """
    audio = M4A(m4a)
    track_name = naming_style.format(**tags_to_names('m4a', audio))
    track_dir = os.path.join( *track_name.split(os.path.sep)[:-1] )
    if not os.path.isdir(track_dir):
        os.makedirs(track_dir)
    
    shutil.copyfile(mp3, track_name)
    if compare_files(mp3, track_name):
        print('Copied {0} to {1} successfully.'.format(mp3, track_name))
    else:
        print('Moving {0} to {1} failed.'.format(mp3, track_name))


def move_mp3(mp3):
    """
    Move the file into its proper directory, according to path.
    
    mp3 - full path to an MP3 file
    """
    audio = EasyMP3(mp3)
    track_name = naming_style.format(**tags_to_names('mp3', audio))
    track_dir = os.path.join( *track_name.split(os.path.sep)[:-1] )
    if not os.path.isdir(track_dir):
        os.makedirs(track_dir)
    
    shutil.copyfile(mp3, track_name)
    if compare_files(mp3, track_name):
        print('Copied {0} to {1} successfully.'.format(mp3, track_name))
    else:
        print('Moving {0} to {1} failed.'.format(mp3, track_name))


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
