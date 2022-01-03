from pytube import Playlist
import os


PLAYLIST_URL = 'https://youtube.com/playlist?list=PLu9sdDMxT8F8Iuzwoiu4ePyfzCwDqTo3p'
RESOLUTION = "720p"

p = Playlist(
    PLAYLIST_URL
)
file_directory = ''
try:
    file_directory += p.title
except KeyError:
    file_directory += "New_PLaylist"

condition = True
while condition:
    try:
        os.makedirs(file_directory)
    except FileExistsError:
        file_directory += '0'
    else:
        condition = False

for video in p.videos:
    stream = video.streams.filter(progressive=True, file_extension="mp4", res=RESOLUTION)
    video_path = os.path.join(os.getcwd(), file_directory)
    if stream:
        stream[0].download(output_path=video_path)
    else:
        with open(os.path.join(video_path, video.title[:10] + ".txt"), 'w') as f:
            f.write(video.title + "------ was not found for mp4 720p\n\n")


