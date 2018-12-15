# coding=utf-8
from moviepy.editor import *

path = r'G:\1'
filename =  ''

L = []
for file in os.listdir(path):
    video = VideoFileClip(os.path.join(path, file))
    L.append(video)

# 拼接视频
final_clip = concatenate_videoclips(L)

# 生成目标视频文件
final_clip.to_videofile(os.path.join(path, filename), fps=24, remove_temp=False)

