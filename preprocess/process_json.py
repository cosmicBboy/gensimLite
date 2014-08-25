# -*- coding: utf-8 -*-

import json
import re


class PreprocessJson(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def loadjson(self):
        with open(self.filepath, 'r') as fp:
            self.json = json.load(fp)

    def removeSymbols(self, text):
        text = re.sub(re.compile('[\W_]+'), ' ', text)
        return ' '.join(text.split())

    def removeNumbers(self, text):
        text = re.sub(re.compile('[0-9]+'), '', text)
        return ' '.join(text.split())

    def processText(self, data):
        text = data.lower()
        text = self.removeSymbols(text)
        return self.removeNumbers(text)

    def processjson(self):
        self.data = self.json[0]
        self.processed = {}
        for key in self.data.keys():
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
    p = PreprocessJson('../../Taxonomy/data/sdsn.json')
    p.loadjson()
    data = p.json[0]
    p.processjson()
    p.savejson('../data/test.json')


    # for key in data.keys()[:1]:
    #     print key
    #     text = data[key].lower()
    #     text = p.removeSymbols(text)
    #     text = p.removeNumbers(text)
    #     print text