# coding=utf-8
import gensim.models.word2vec as word2vec
import gensim
import logging
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.LineSentence('enwik8')

model=gensim.models.Word2Vec(sentences,sg=0,size=200,window=5,min_count=5,negative=0,hs=1,workers=4)

# model.wv.index2word

model.save('model\\cbow_hs')

model1 = gensim.models.Word2Vec.load('model\\cbow_hs')
model2 = gensim.models.Word2Vec.load('model\\cbow_neg')
model3 = gensim.models.Word2Vec.load('model\\sg_hs')
model4 = gensim.models.Word2Vec.load('model\\sg_neg')

f1 = open('compare.txt')
S = f1.readlines()
f2 = open('result.txt', 'w')

dat = pd.DataFrame(columns=['base', 'cbow_hs', 'cbow_neg', 'sg_hs', 'sg_neg'])
for i in range(len(S)):
    c = S[i].split()
    l = [float(c[-1])]
    l.append(model1.similarity(c[0], c[1]))
    l.append(model2.similarity(c[0], c[1]))
    l.append(model3.similarity(c[0], c[1]))
    l.append(model4.similarity(c[0], c[1]))
    dat = dat.append(dict(zip(['base', 'cbow_hs', 'cbow_neg', 'sg_hs', 'sg_neg'], l)), ignore_index=True)

f2.write(str(dat.corr()))
f2.write('\n')
for i in range(len(S)):
    c = S[i].split()
    f2.write(c[0])
    f2.write('\t')
    f2.write(c[1])
    f2.write('\t')
    f2.write('\t'.join([str(s) for s in dat.iloc[i]]))
    f2.write('\n')
