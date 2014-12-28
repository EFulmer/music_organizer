# example:
# '/Users/eric/Music/{artist_name}/{album_name}/{track_num:0{zero_padding}}-{track_title}.{ext}'.format(artist_name='Oasis', album_name='Definitely Maybe', track_num=3, zero_padding=2, track_title='Live Forever', ext='mp3')
# TODO: make OS-agnostic; i.e. list as such ['Users', 'eric', 'Music', '{artist_name}',] etc.

zero_padding = 2
naming_style = '/Users/eric/Music/{artist_name}/{album_name}/{track_num:0>{zero_padding}}-{track_title}{ext}'
