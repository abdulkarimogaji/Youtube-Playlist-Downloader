A simple youtube playlist downloader using pythons's pytube module

- saves all the videos in a directory same as the current working directory and named as the title of the playlist
- if title of playlist fails to fetch replace with "New_PLaylist"
- appends "0" as necessary to make the directory unique
- should work for all OSs because of python's  `os.getcwd()` and `os.path.joinpath()`
- Threading and queuing implemented

New-Feature To Add:

- automatically download a lower resolution when higher resolution is not available