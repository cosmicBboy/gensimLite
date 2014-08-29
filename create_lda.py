# -*- coding: utf-8 -*-

import logging
from gensim import models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


class LdaModel(object):

    def __init__(self, corpus, dictionary):
        '''
        Sets paramaeter values in dictionary to be
        passed into LdaModel instantiation method from gensim
        '''
        self.params = {}
        self.params['corpus'] = corpus
        self.params['id2word'] = dictionary

    def setParams(self, paramDictionary):

        for param, value in paramDictionary.items():
            self.params[param] = value
        return self

    def streamParams(self, num_topics, update_every=1,
                     chunksize=10000, passes=10):
        params = locals()
        del params['self']
        return params

    def batchParams(self, num_topics, update_every=0, passes=20):
        params = locals()
        del params['self']
        return params

    def runLda(self):
        self.model = models.ldamodel.LdaModel(**self.params)
        return self

if __name__ == "__main__":
    from create_corpus import GensimCorpus
    g = GensimCorpus()
    dictionary = g.loadDictionary('data/sdsn.dict')
    corpus = g.loadCorpus('data/sdsn.mm')
    lda = LdaModel(corpus, dictionary)

    #get default stream params
    params = lda.streamParams(num_topics=12, passes=20)
    lda.setParams(params).runLda()
