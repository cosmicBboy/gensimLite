# -*- coding: utf-8 -*-
"""
Function wrapper for performing tasks in
the gensim metatopic pipeline
"""

from process_json import Preprocessor
from create_corpus import GensimCorpus
from create_lda import LdaModel


def preprocess(input_fp, output_fp):
    p = Preprocessor(input_fp)
    p.loadjson()
    p.processjson()
    p.savejson(output_fp)


def dictionaryGen(data_fp, dict_fp):
    '''
    generates a gensim dictionary
    and saves to dict_fp
    '''
    g = GensimCorpus(data_fp)
    #loads data object as json and converts to tuple
    g.loadjson().json2tuple()
    #tokenize data
    g.tokenizeData()
    #create dictionary and filter lower word frequency
    print 'creating dictionary...'
    g.createDictionary().filterFrequency(n=1)
    #save dictionary
    print 'saving dictionary to %s' % dict_fp
    g.saveDictionary(dict_fp)


def corpusGen(data_fp, dict_fp, corpus_fp):
    '''
    generates a gensim corpus using
    gensim dictionary file
    '''
    #load data
    g = GensimCorpus(data_fp)
    g.loadjson().json2tuple()
    #tokenize data
    g.tokenizeData()
    #load dictionary
    g.loadDictionary(dict_fp)
    #create corpus
    print 'creating corpus...'
    g.createCorpus([text for tag, text in g.data])
    #save corpus
    print 'saving corpus to %s' % dict_fp
    g.saveCorpus(corpus_fp)


def ldaGen(dict_fp, corpus_fp, model_fp,
           streamParameters=None, batchParameters=None):
    g = GensimCorpus()
    dictionary = g.loadDictionary(dict_fp)
    corpus = g.loadCorpus(corpus_fp)
    lda = LdaModel(corpus, dictionary)

    #get params
    if streamParameters:
        params = lda.streamParams(**streamParameters)
    elif batchParameters:
        params = lda.batchParams(**batchParameters)
    else:
        print 'please specify streaming or batch lda'

    #set params and run model
    lda.setParams(params)
    lda.runLda()
    lda.save_model(model_fp)
    return lda


if __name__ == "__main__":

    #### preprocess data specifying input and output
    #preprocess('../Taxonomy/data/sdsn2.json', 'data/sdsn2.json')
    #dictionaryGen('data/sdsn2.json', 'data/sdsn2.dict')
    #corpusGen('data/sdsn2.json', 'data/sdsn2.dict', 'data/sdsn2.mm')
    params = {'num_topics': 12, 'update_every': 1,
              'passes': 1, 'chunksize': 10000}

    lda = ldaGen(dict_fp='data/sdsn2.dict',
                 corpus_fp='data/sdsn2.mm',
                 model_fp='data/sdsn2.lda_model',
                 streamParameters=params)