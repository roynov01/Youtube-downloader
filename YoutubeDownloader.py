from pytube import YouTube
from pytube import Playlist
from moviepy.editor import *
import os


def mp4_to_mp3(file_in, file_out):
    """convert mp3 into mp4"""
    video_clip = VideoFileClip(file_in)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(file_out)
    audio_clip.close()
    video_clip.close()


def download_track(link, directory, download_type):
    """a function that downloads a music track from YT. for video = download_type=22"""
    try:
        youtube_video = YouTube(link)
        youtube_video = youtube_video.streams.get_by_itag(download_type)
        youtube_video.download(directory)
    except:
        raise Exception


def list_dir(directory):
    """makes a list of file names inside a given folder"""
    filenames = os.listdir(directory)
    return filenames


def download_playlist(link, directory):
    """download entire YT playlist"""
    playlist = Playlist(link)
    for track in playlist.videos:  # actual download
        track.streams.first().download(directory)


def convert(directory):
    """convert mp3 into mp4 in the same directory"""
    files = list_dir(directory)
    for file in files:
        mp4_to_mp3(directory + "//" + file, directory + '//' + file[:-4] + '.mp3')
        os.chdir(directory)  # now delete mp4 files
        os.unlink(file)


if __name__ == "__main__":
    pass
