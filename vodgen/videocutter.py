import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import VideoClip

def createVideo(originalFile, startTime, endTime, resultFile, codec=None):
    if(codec != None):
        call = f"echo y|ffmpeg -i {originalFile} -vcodec  -ss {startTime} -to {endTime} -c:v copy -c:a copy {resultFile}"
        os.system(call)

    originalVideoClip = VideoClip(originalFile)

    video = originalVideoClip.subclip(startTime, endTime)

    video.write_videofile(resultFile, verbose=False, logger=None)


