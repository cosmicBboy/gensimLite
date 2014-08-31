# -*- coding: utf-8 -*-
"""
Create Gensim mmCorpus
"""

from gensim import corpora
import json


class GensimCorpus(object):

    def __init__(self, datafp=None):
        try:
            self.datafp = datafp
        except:
            pass

    def loadjson(self):
        '''loads a json file'''
        with open(self.datafp, 'r') as f:
            self.data = json.load(f)
        if isinstance(self.data, list):
            print 'json converted to list object'
            #if json list contains only one element
            #reassigns self.data to inner object
            if len(self.data) == 1:
                self.data = self.data[0]
        return self

    def json2tuple(self):
        '''converts json object to tuple'''
        self.data = self.data.items()
        return self

    def tokenizeData(self):
        tokenized = [(tag, self.tokenizeText(text)) for tag, text in self.data]
        self.data = tokenized
        return self

    def tokenizeText(self, text, sep=' '):
        '''helper function for json2tuple method'''
        return text.split(sep)

    def createDictionary(self):
        '''creates a dictionary object'''
        self.dictionary = corpora.Dictionary([text for tag, text in self.data])
        return self

    def filterFrequency(self, n=1):
        '''filters dictionary object by removing
        tokens with a frequency of n or lower'''
        #get token ids of tokens that pass the filter
        freq_ids = [tokenid for tokenid, docfreq
                    in self.dictionary.dfs.iteritems()
                    if docfreq <= n]
        #uses gensim's filter_tokens method to remove once_ids
        self.dictionary.filter_tokens(freq_ids)
        #remove gaps in id sequence after filtration
        self.dictionary.compactify()
        return self

    def saveDictionary(self, fp):
        '''saves dictionary to filepath'''
        assert self.dictionary, 'GensimCorpus dictionary not specified'
        self.dictionary.save('%s' % fp)

    def loadDictionary(self, fp):
        '''loads dictionary from filepath'''
        self.dictionary = corpora.Dictionary.load('%s' % fp)
        return self.dictionary

    def createCorpus(self, data):
        '''
        creates a corpus in Market Matrix format, consisting of a list of
        vector tuple arrays, each vector representing a document, and each
        tuple representing the token id and document frequency in that order.

        data must be a list of documents, each document being a tokenized list

        Only use for smaller corpuses (~10000 or less)
        '''
        assert self.dictionary, 'dictionary not specified. please\
            load or create a dictionary'
        self.corpus = [self.dictionary.doc2bow(d) for d in data]
        return self

    def createCorpusStream(self):
        '''
        creates a corpus stream in Market Matrix format that loads each
        document into memory one at a time, such that the streamCorpus
        method iterates through a text file where each document is a line.

        This method can be extended to other file formats, such as
        dictionaries, json, and csv.
        '''
        self.corpusStream = None
        pass

    def loadCorpus(self, fp):
        '''
        Loads corpus in Market Matrix format
        '''
        self.corpus = corpora.MmCorpus(fp)
        return self.corpus

    def corpusLength(self):
        '''
        Gets length of corpus
        '''
        assert self.corpus, 'corpus is not specified'
        corpusLength = 0
        for d in self.corpus:
            corpusLength += 1
        return corpusLength

    def saveCorpus(self, fp):
        '''
        Saves corpus to Market Matrix format
        '''
        corpora.MmCorpus.serialize(fp, self.corpus)
        return self

    def head(self, n=1):
        '''prints first n data points'''
        print self.data[:n]

if __name__ == "__main__":
    datafp = 'data/sdsn.json'
    g = GensimCorpus(datafp)
    g.loadjson().json2tuple()
    for k, v in g.data:
        print k

    #### tokenize the text data
    #g.tokenizeData()

    #### create dictionary and filter
    #g.createDictionary().filterFrequency(n=1)

    #### save dictionary`
    #g.saveDictionary('data/sdsn.dict')

    ##### load dictionary
    #g.loadDictionary('data/sdsn.dict')

    #### create in-memory corpus
    #texts = [text for tag, text in g.data]
    #g.createCorpus(texts)

    #### save corpus
    #g.saveCorpus('data/sdsn.mm')

    #### load corpus
    #g.loadCorpus('data/sdsn.mm')
    #g.corpusLength()
