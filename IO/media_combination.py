# coding=utf-8
# 用于合并视频
from moviepy.editor import *

root = ''       # 将目录下的所有文件合并为一个视频
filename =  ''      # 最终视频名称

L = []
for file in os.listdir(root):
    video = VideoFileClip(os.path.join(root, file))
    L.append(video)

# 拼接视频
final_clip = concatenate_videoclips(L)

# 生成目标视频文件,remove_temp指是否删除原视频文件
final_clip.to_videofile(os.path.join(root, filename), fps=24, remove_temp=False)

