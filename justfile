
each:
    manim -ql -p video.py EachPart

overview:
    manim -ql -p video.py Overview

all:
    manim -aqh video.py

alias t := transcode

transcode:
    ffmpeg -i media/videos/video/1080p60/EachPart.mp4 -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p -c:a copy videos/EachPart.mov

re-transcode:
    ffmpeg -i electron_microscopy.mov -c:a copy -c:s mov_text electron_microscopy.mp4
