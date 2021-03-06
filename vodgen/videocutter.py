"""Cuts video"""
import os
import threading

#from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import subprocess

def create_video(original_file, start_time, end_time, result_file, codec=""):
    """
    Creates a video based on given parameters, has experiemntal mode if given the codec argument
    """
    start_time = start_time[:len(start_time) - 3]
    end_time = end_time[:len(end_time) - 3]
    print("Received: " + codec)
    if codec != "":
        # pylint: disable=line-too-long
        subprocess.call(["ffmpeg", "-i", original_file, "-ss", start_time, "-to", end_time, "-c:v", codec, "-c", "copy", "-copyts", result_file])
    else:
        #moviepy_implementation(original_file, start_time, end_time, result_file)
        threading.Thread(target=moviepy_implementation, args=(original_file, start_time, end_time, result_file))

def moviepy_implementation(original_file, start_time, end_time, result_file):
    original_video_clip = VideoFileClip(original_file)

    video = original_video_clip.subclip(start_time, end_time)

    video.write_videofile(result_file, verbose=False, logger=None)
