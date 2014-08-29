# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
import json
import re

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

sdsnStopWords = ['global',
                 'development',
                 'sustainable',
                 'sustainably',
                 ]


class PreprocessJson(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def loadjson(self):
        with open(self.filepath, 'r') as fp:
            self.json = json.load(fp)
        return self

    def removeSymbols(self, text):
        text = re.sub(re.compile('[\W_]+'), ' ', text)
        return ' '.join(text.split())

    def removeNumbers(self, text):
        text = re.sub(re.compile('[0-9]+'), '', text)
        return ' '.join(text.split())

    def removeStopwords(self, text):
        text = [w for w in text.split() if not w in stopwords.words('english')]
        return ' '.join(text)

    def removeWordlist(self, text, wordList=sdsnStopWords):
        text = [w for w in text.split() if not w in wordList]
        return ' '.join(text)

    def minCharFilter(self, text, n=2):
        '''filters out text equal to or below specified threshold'''
        text = [w for w in text.split() if len(w) > n]
        return ' '.join(text)

    def maxCharFilter(self, text, n=25):
        '''filters out text above specified character length'''
        text = [w for w in text.split() if len(w) <= n]
        return ' '.join(text)

    def processText(self, data, removeStopwords=True):
        text = self.removeSymbols(data.lower())
        text = self.removeNumbers(text)
        if removeStopwords is True:
            text = self.removeStopwords(text)
        text = self.removeWordlist(text)
        text = self.minCharFilter(text)
        text = self.maxCharFilter(text)
        return text

    def processjson(self):
        self.data = self.json[0]
        self.processed = {}
        count = 0
        for key in self.data.keys():
            count += 1
            print 'processing document %d...' % count
            text = self.processText(self.data[key])
            self.processed[key] = text

    def savejson(self, filepath):
        with open(filepath, 'w') as fp:
            json.dump([self.processed], fp)

    def printdata(self):
        for k, v in self.processed.items():
            print '---------------------\n%s\n---------------------' % k
            print v
            print '\n'

if __name__ == "__main__":
    p = PreprocessJson('../Taxonomy/data/sdsn.json')
    p.loadjson()
    p.processjson()
    #p.savejson('data/sdsn2.json')

    # for key in data.keys()[:1]:
    #     print key
    #     text = data[key].lower()
    #     text = p.removeSymbols(text)
    #     text = p.removeNumbers(text)
    #     print text