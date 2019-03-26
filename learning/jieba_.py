# coding=utf-8
import jieba

l1 = '全国计算机等级考试'
l2 = jieba.lcut(l1)
l3 = jieba.lcut(l1, cut_all=True)
jieba.add_word('计算机等级考试')
l4 = jieba.lcut(l1)