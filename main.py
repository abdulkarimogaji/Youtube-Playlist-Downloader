from pytube import Playlist
import os
from queue import Queue
from threading import Thread
from time import perf_counter

running = False


def progress_func(_s, _chunk, bytes_remaining):
    print(f"\r{str(bytes_remaining // 1000000)}.{str((bytes_remaining % 1000000) // 1000)}MB left", end="")


def complete_func(_, file_path):
    print(f"\nDownload Complete | {file_path.strip('src')[-1][1:]}")


def make_directory(playlist):
    file = ''
    try:
        file += playlist.title
    except KeyError:
        file += "New_Playlist"

    condition = True
    while condition:
        try:
            os.makedirs(file)
        except FileExistsError:
            file += '0'
        else:
            condition = False
    return file


def download_streams(queue_list):
    while running:
        s = queue_list.get()
        try:
            s.download()
        finally:
            queue_list.task_done()


if __name__ == "__main__":
    running = True
    PLAYLIST_URL = input("Paste the url of the youtube playlist you want to download and press enter\n")
    p = Playlist(PLAYLIST_URL)

    # make playlist directory
    file_directory = make_directory(p)
    print(f"...{p.length} videos found...")
    print("Type in the resolution you want to download")
    RESOLUTION = input("[360p, 720p, 128p]\n").lower()
    print("Type the format")

    FORMAT = input("[mp4, None]\n").lower()

    # start timer
    t = perf_counter()

    # create queue
    queue_of_downloads = Queue()

    for video in p.videos[:6]:
        video.register_on_progress_callback(progress_func)
        video.register_on_complete_callback(complete_func)
        stream = video.streams.filter(progressive=True, file_extension=FORMAT, res=RESOLUTION)
        video_path = os.path.join(os.getcwd(), file_directory)
        global save_path
        save_path = video_path
        if stream:
            # populate queue
            queue_of_downloads.put(stream[0])
            print("setting...... " + video.title)
        else:
            with open(os.path.join(video_path, video.title[:10] + ".txt"), 'w') as f:
                f.write(video.title + f"------ was not found for mp4 {FORMAT}\n\n")

    # create threads
    for _ in range(4):
        worker = Thread(target=download_streams, kwargs={"queue_list": queue_of_downloads}, daemon=True).start()

    # join queue
    queue_of_downloads.join()

    print(f"Playlist Download Completed in {perf_counter() - t}, playlist saved at \"{save_path}\"")




