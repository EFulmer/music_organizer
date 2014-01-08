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

from audio_formats import audio_formats
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
    # TODO just straight up copy and compare non-audio files (album 
    # art etc) or something; poss. rename fn to reflect change.
    fmt = os.path.splitext(audio)[1]
    tags = tags_to_names(fmt, audio)
    track_name = naming_style.format(**tags)
    track_dir = os.path.dirname(track_name)
    if not os.path.isdir(track_dir):
        os.makedirs(track_dir)
    
    shutil.copyfile(audio, track_name)
    if compare_files(audio, track_name):
        print('Copied {0} to {1} successfully.'.format(audio, track_name))
    else:
        print('Moving {0} to {1} failed.'.format(audio, track_name))


def tags_to_names(fmt, song):
    """
    Convert the tag names from fmt to the names used to rename the music file.
    """
    names = {}
    names['ext'] = fmt
    names['zero_padding'] = zero_padding
    if fmt == '.flac':
        # Keys for tags:
        # 'date': year of release
        # 'album': album title
        # 'title': track title
        # 'tracknumber': track number (how does it handle total tracks?)
        # 'artist': artist name
        # TODO: Flac is being funny (i.e. [u'Bob Dylan'] not 'Bob 
        # Dylan'. Fix it
        metadata = FLAC(song)
        names['artist_name'] = metadata[u'artist'][0]
        names['album_name'] = metadata[u'album'][0]
        names['track_num'] = metadata[u'tracknumber'][0]
        names['track_title'] = metadata[u'title'][0]
        pass
    elif fmt == '.m4a':
        # Keys for tags:
        # 'cpil': Is this track part of a compilation?
        # 'disk': (on disk #, of # disks)
        # 'purd': purchase date
        # 'soal': song album
        # 'soar': song artist
        # 'sonm': song title
        # 'trkn': (track #, out of #)
        metadata = M4A(song)
        names['artist_name'] = metadata[u'soar']
        names['album_name'] = metadata[u'soal']
        names['track_num'] = metadata[u'trkn'][0]
        names['track_title'] = metadata[u'sonm']
    elif fmt == '.mp3':
        # Keys for EasyMP3 tags:
        # 'album' - str list; album name
        # 'performer' - str list; is this album artist or regular artist or what?
        # 'artist' - str list; see above
        # 'title' - str list; the song's title
        # 'date' - str list; date the song was released
        # 'tracknumber' - str list; track #/total tracks
        # 'disknumber' - str list; disk #
        metadata = EasyMP3(song)
        names['artist_name'] = metadata[u'artist'][0]
        names['album_name'] = metadata[u'album'][0]
        names['track_num'] = int(metadata[u'tracknumber'][0])
        names['track_title'] = metadata[u'title'][0]
    else:
        raise ValueError('expected music format name')
    return names


def organize_files(folder):
    """
    Move all audio files in folder (not including its subdirectories) 
    to the user's music library.

    folder - full path to directory containing audio files
    """
    
    # TODO this is ugly.
    # probably want to just copy non-audio files without anything 
    # special being done.
    songs = [ os.path.join(folder, f) for f in os.listdir(folder) 
              if os.path.isfile(os.path.join(folder, f)) 
              and os.path.splitext(f)[1] in audio_formats ]

    others = [ os.path.join(folder, f) for f in os.listdir(folder)
               if os.path.isfile(os.path.join(folder, f))
               and os.path.splitext(f)[0] not in audio_formats ]
    for f in songs:
        move_audio(f)


def main():
    for folder in sys.argv[1:]:
        organize_files(folder)


if __name__ == '__main__':
    main()
