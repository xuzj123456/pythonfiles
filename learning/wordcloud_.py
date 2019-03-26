# coding=utf-8
from wordcloud import WordCloud

s = 'I am a student. I like python.'
w = WordCloud().generate(s)
w.to_file('a.png')