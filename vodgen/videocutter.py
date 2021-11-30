"""Cuts video"""
import os

#from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import VideoClip

def create_video(original_file, start_time, end_time, result_file, codec=None):
    """
    Creates a video based on given parameters, has experiemntal mode if given the codec argument
    """
    if codec is not None:
        # pylint: disable=line-too-long
        call = f"echo y|ffmpeg -i {original_file} -vcodec  -ss {start_time} -to {end_time} -c:v copy -c:a copy {result_file}"
        os.system(call)

    original_video_clip = VideoClip(original_file)

    video = original_video_clip.subclip(start_time, end_time)

    video.write_videofile(result_file, verbose=False, logger=None)
