music_organizer
===============

Small Python script that organizes music files. Currently, it organizes them like so: ~\Music\ArtistName\AlbumName\00-SongTitle.mp3.

Only tested with Python 2.7.5 on OS X Mavericks so far (let me know if you use it and find any issues on other systems!). Planned improvements include supporting user-defined folder/file hierarchies, and support for other audio formats.

Use like so:

    python music_organizer folder_that_contains_the_music

Requires [Mutagen](https://code.google.com/p/mutagen/).
