import unittest

from mutagen import EasyMP3

import music_organizer

# TODO: Constants for test file name and expected output file's name.
NUM_TESTS = 1
TEST_FILES = [ 'mp3test{0}.mp3'.format(i) for i in range(NUM_TESTS) ]

class MP3Tests(unittest.TestCase):
    
    """Tests for MP3 files."""
    def test_tags(self):
        """Tests that copied files retain proper tags."""
        # TODO: layout of function: reorg test file, check copy's tags
        # against orig file's.
        pass


    def tearDown(self):
        """Delete test file."""
        # TODO: should delete test file.
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
